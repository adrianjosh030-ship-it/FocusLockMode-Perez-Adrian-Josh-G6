from django.conf import settings
from django.db import models


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="focus_categories")
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ("user", "name")
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class FocusSession(models.Model):
    PLANNED, ACTIVE, COMPLETED, ABANDONED = "planned", "active", "completed", "abandoned"
    STATUS_CHOICES = [(PLANNED, "Planned"), (ACTIVE, "Active"),
                      (COMPLETED, "Completed"), (ABANDONED, "Abandoned")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="focus_sessions")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions")
    title = models.CharField(max_length=120)
    planned_minutes = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PLANNED)
    notes = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.status})"
