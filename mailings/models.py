from django.db import models
from django.contrib.auth import get_user_model

from config.dry import NULLABLE


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(**NULLABLE)

    class Meta:
        permissions = [
            ("view_client_custom", "Can view client"),
        ]

    def __str__(self):
        return self.email


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    class Meta:
        permissions = [
            ("view_message_custom", "Can view message"),
        ]

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Created', 'Created'),
        ('Started', 'Started'),
        ('Completed', 'Completed'),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("view_mailing_custom", "Can view mailing"),
        ]

    def __str__(self):
        return f"Mailing {self.id}"


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('Success', 'Success'),
        ('Failure', 'Failure'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response = models.TextField(**NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Attempt {self.id} for Mailing {self.mailing.id}"
