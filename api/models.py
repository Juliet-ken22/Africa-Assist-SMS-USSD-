from django.db import models

class Message(models.Model):
    TYPE_CHOICES = [
        ('LEARN', 'Learn'),
        ('FARM', 'Farm'),
        ('HEALTH', 'Health'),
        ('OTHER', 'Other'),
    ]
    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('Luganda', 'Luganda'),
        ('Swahili', 'Swahili'),
        ('Runyankole', 'Runyankole'),
        ('Acholi', 'Acholi'),
    ]
    phone = models.CharField(max_length=20)
    message_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='English')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {self.message_type} - {self.language} - {self.created_at}"