from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from config.dry import NULLABLE


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, verbose_name='Фамилия и инициалы')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')

    class Meta:
        permissions = [
            ("view_client_custom", "Can view client"),
        ]

    def __str__(self):
        return self.email


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема')
    body = models.TextField(verbose_name='Сообщение')

    class Meta:
        permissions = [
            ("view_message_custom", "Can view message"),
        ]

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Created', 'Создано'),
        ('Started', 'Запущенно'),
        ('Completed', 'Завершено'),
    ]

    start_time = models.DateTimeField(verbose_name='когда запустить рассылку')
    end_time = models.DateTimeField(verbose_name='когда закончить рассылку')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='какое сообщение?')
    clients = models.ManyToManyField(Client, verbose_name='кому отправить?')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("view_mailing_custom", "Can view mailing"),
        ]

    def __str__(self):
        return f"Mailing {self.id}"


@receiver(post_save, sender=Mailing)
def update_mailing_status(sender, instance, created, **kwargs):
    if created:
        instance.status = 'Created'
        instance.save()
    elif instance.start_time <= timezone.now() <= instance.end_time:
        instance.status = 'Started'
        instance.save()
    elif timezone.now() > instance.end_time:
        instance.status = 'Completed'
        instance.save()


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('Success', 'Успешно'),
        ('Failure', 'Не удалось'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response = models.TextField(**NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Attempt {self.id} for Mailing {self.mailing.id}"
