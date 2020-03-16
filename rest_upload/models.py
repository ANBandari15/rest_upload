from django.db import models


class Document(models.Model):

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents", max_length=100, blank=True)

    def __unicode__(self):
        return self.title
