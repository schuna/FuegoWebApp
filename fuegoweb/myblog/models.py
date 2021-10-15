from django.db import models
from django.utils.timezone import now
from django.conf import settings


class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000)
    image_path = models.CharField(max_length=255, unique=True)
    updated_time = models.DateTimeField(default=now)
    user_id = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.description}, {settings.BASE_DIR}"
