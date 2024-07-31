from django.conf import settings
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class LikedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Type (Product, video, article) and ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # It could have been done by importing products from playground models
    # but that won't be professional enough, hence, the use of content_type.
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey()
