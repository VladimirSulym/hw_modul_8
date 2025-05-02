from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter

from lms.models import Course, Lesson, Payment, Subscription, CoursePayment
from lms.paginators import MyPagination
from lms.permissions import IsModerators, IsOwner
from lms.serializers import (
    CourseDetailSerializer,
    CourseSerializer,
    LessonSerializer,
    PaymentSerializer,
    SubscriptionSerializer,
    CoursePaymentSerializer,
)
from lms.services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
)

from lms.tasks import send_mail_user


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для работы с моделью Course"""

    # serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                ~IsModerators,
                permissions.IsAuthenticated,
            )
        elif self.action in [
            "update",
            "retrieve",
        ]:
            self.permission_classes = (
                IsModerators | IsOwner,
                permissions.IsAuthenticated,
            )
        elif self.action == "delete":
            self.permission_classes = (
                ~IsModerators,
                permissions.IsAuthenticated,
                IsOwner,
            )
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """API-вью для создания нового урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    permission_classes = [
        # permissions.AllowAny,
        ~IsModerators,
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        if lesson.course.sub.all().exists():
            subscriber_ids = list(lesson.course.sub.values_list("id", flat=True))
            send_mail_user.delay(
                "добавлен", lesson.course.title, lesson.title, subscriber_ids
            )
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """API-вью для получения списка всех уроков конкретного курса"""

    serializer_class = LessonSerializer
    # permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    queryset = Lesson.objects.all()
    pagination_class = MyPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """API-вью для получения информации о конкретном уроке"""

    serializer_class = LessonSerializer
    # permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    queryset = Lesson.objects.all()
    permission_classes = (
        IsModerators | IsOwner,
        permissions.IsAuthenticated,
    )


class LessonUpdateAPIView(generics.UpdateAPIView):
    """API-вью для изменения информации о конкретном уроке"""

    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    # Разрешает запрос только администраторам
    serializer_class = LessonSerializer
    # permission_classes = [permissions.AllowAny]  # Разрешает запрос всем пользователям
    queryset = Lesson.objects.all()
    permission_classes = (
        # permissions.AllowAny,
        IsModerators | IsOwner,
        permissions.IsAuthenticated,
    )

    def perform_update(self, serializer):
        lesson = serializer.save()
        if lesson.course.sub.all().exists():
            subscriber_ids = list(lesson.course.sub.values_list("id", flat=True))
            send_mail_user.delay(
                "обновлен", lesson.course.title, lesson.title, subscriber_ids
            )
        lesson.save()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """API-вью для удаления урока"""

    # permission_classes = [permissions.AllowAny]  # Разрешает запрос всем пользователям
    queryset = Lesson.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )

    def perform_destroy(self, instance):
        if instance.course.sub.all().exists():
            subscriber_ids = list(instance.course.sub.values_list("id", flat=True))
            send_mail_user.delay(
                "удален", instance.course.title, instance.title, subscriber_ids
            )
        instance.delete()


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    """API-вью для получения информации о конкретном уроке"""

    serializer_class = CourseDetailSerializer
    # permission_classes = [permissions.AllowAny] # Разрешает запрос всем пользователям
    queryset = Course.objects.all()
    permission_classes = (
        IsModerators | IsOwner,
        permissions.IsAuthenticated,
    )


class PaymentListAPIView(generics.ListAPIView):
    """API-вью для получения списка всех платежей пользователя"""

    serializer_class = PaymentSerializer
    # permission_classes = [permissions.AllowAny] # Разрешает запрос только авторизованным пользователям
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    search_fields = [
        "amount",
    ]
    filterset_fields = ["course", "payment_type"]
    ordering_fields = ["payment_date"]


class SubscriptionAPIView(generics.CreateAPIView):
    """API-вью для подписки на курс"""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
        # Возвращаем ответ в API
        return Response({"message": message})


class CoursePaymentCreateAPIView(generics.CreateAPIView):
    """API-вью для оплаты курсов"""

    serializer_class = CoursePaymentSerializer
    queryset = CoursePayment.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = create_stripe_product(name=payment.course.title)
        price = create_stripe_price(amount=payment.amount, product=product)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
