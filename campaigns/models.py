from django.db import models

class Campaign(models.Model):
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    engagement_score = models.IntegerField(default=0, help_text="Score from 0 to 100")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.platform})"
