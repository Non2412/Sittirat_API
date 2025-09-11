from django.db import models


# Minimal models file for the api app (placeholder)
class Placeholder(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Placeholder'
        verbose_name_plural = 'Placeholders'
