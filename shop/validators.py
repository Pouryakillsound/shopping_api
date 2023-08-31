from django.core.exceptions import ValidationError

def image_maximum_file_size(file):
    MAX_SIZE = 10240 * 1024
    if file.size > MAX_SIZE:
        raise ValidationError('File is so big')
    return file