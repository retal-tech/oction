from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Projects(TranslatableModel):
    """
    Projects model
    """
    translations = TranslatedFields(
        title=models.CharField(max_length=90),
        description=models.TextField(),
        image=models.ImageField(upload_to='projects/'),
        url=models.URLField(blank=True, null=True),
    )

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
