from django.db import models

class Project(models.Model):
    user_id = models.IntegerField(db_index=True)  # ID from auth_service JWT
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
