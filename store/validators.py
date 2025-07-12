import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Şifre en az 1 büyük harf içermelidir"),
                code="password_no_upper",
            )
        if not re.search(r'\d', password):
            raise ValidationError(
                _("Şifre en az 1 sayı içermelidir"),
                code='password_no_number',
            )
    def get_help_text(self):
        return _(
            "Şifre en az bir büyük harf ve bir sayı içermelidir."
        )