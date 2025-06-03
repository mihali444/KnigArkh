from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

def validate_file_size(value):
    """Валидатор для проверки размера файла (максимум 5MB)"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB в байтах
        raise ValidationError(_('Максимальный размер файла 5MB'))

def validate_image_extension(value):
    """Валидатор для проверки расширения файла"""
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    validator = FileExtensionValidator(allowed_extensions=allowed_extensions)
    validator(value) 