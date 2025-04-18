import re
from rest_framework.serializers import ValidationError


class DataInputValidator:
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        result_list_description = re.findall(
            r"[a-zA-Z0-9]+\.[a-zA-Z]+", value.get(self.fields), flags=re.IGNORECASE
        )
        for result in result_list_description:
            if result != "youtube.com":
                raise ValidationError(
                    "Содержит недопустимую ссылку на материалы в описании"
                )
