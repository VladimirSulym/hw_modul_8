from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        moderators_group, creates = Group.objects.get_or_create(name="moderators")
        view_permission_course = Permission.objects.get(codename="view_course")
        view_permission_lesson = Permission.objects.get(codename="view_lesson")
        moderators_group.permissions.add(view_permission_course, view_permission_lesson)

        for index, user in enumerate(User.objects.all()):
            if index % 2:
                user.groups.add(moderators_group)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Пользователю {user.email} назначена группа {moderators_group}"
                    )
                )
