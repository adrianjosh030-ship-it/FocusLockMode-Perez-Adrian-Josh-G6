from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Custom user with a role. Rename the roles below to fit your system."""

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        STUDENT = "student", "Student"

    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    contact_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(r"^[0-9+\-\s()]{7,20}$", "Enter a valid contact number.")],
    )
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)

    def save(self, *args, **kwargs):
        # Superusers (createsuperuser) are always Admins.
        if self.is_superuser:
            self.role = self.Role.ADMIN
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
