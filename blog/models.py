from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor.fields import RichTextField


def validate_file_extention(value):
    from django.core.exceptions import ValidationError
    import os

    ext = os.path.splitext(value.name)[1]
    valid_exts = [".png", ".jpg"]
    if ext not in valid_exts:
        raise ValidationError("Unsupported file exception!")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(
        upload_to="files/user_avatar/", null=False, blank=False, validators=[validate_file_extention]
    )
    description = models.CharField(max_length=512, null=False, blank=False)

    def __str__(self) -> str:
        return self.user.first_name + " " + self.user.last_name


class Article(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    cover = models.FileField(
        upload_to="files/article_cover/", null=False, blank=False, validators=[validate_file_extention]
    )
    content = RichTextField()
    created_at = models.DateTimeField(default=datetime.now(), blank=False)
    # TODO: what is foreignkey?
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    author = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    cover = models.FileField(
        upload_to="files/category_cover", null=False, blank=False, validators=[validate_file_extention]
    )

    def __str__(self) -> str:
        return self.title
