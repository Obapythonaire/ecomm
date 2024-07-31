from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label

class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type (Product, video, article) and ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # It could have been done by importing products from playground models
    # but that won't be professional enough, hence, the use of content_type.
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey()
