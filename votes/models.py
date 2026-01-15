from django.db import models


class Vote(models.Model):
    CANDIDATE_CHOICES = [
        ("mj", "Michael Jordan"),
        ("lebron", "LeBron James"),
    ]

    voter_name = models.CharField(max_length=150)
    candidate = models.CharField(max_length=16, choices=CANDIDATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.voter_name} -> {self.candidate}"
from django.db import models

# Create your models here.
