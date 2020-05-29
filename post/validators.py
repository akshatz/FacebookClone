import os

from django.core.exceptions import ValidationError


def validate_file_extension(value):
    try:
        valid_extensions = ['mp4']
    except:
        raise ValidationError('Unsupported file extension.')