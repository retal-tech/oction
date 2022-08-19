from ast import mod
from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Projects(TranslatableModel):
    """
    Projects model
    """
    translations = TranslatedFields(
        title=models.CharField(max_length=90),
        description=models.TextField(),
    )
    pdf =  models.FileField(upload_to='products/', default=None)
    priority = models.IntegerField(default=0)


    def __str__(self):
        return self.title


class Contact(models.Model):
    """
    Contact model
    """
    name = models.CharField(max_length=90)
    email = models.EmailField()
    subject = models.CharField(max_length=90, blank=True, null=True)
    message = models.TextField()

    def __str__(self):
        return self.name
