from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from mailings.models import Mailing, MailingAttempt


class Command(BaseCommand):
    help = 'Send mailings'

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status='Started')
        for mailing in mailings:
            if mailing.start_time <= timezone.now() <= mailing.end_time:
                for client in mailing.clients.all():
                    try:
                        send_mail(
                            mailing.message.subject,
                            mailing.message.body,
                            'from@example.com',
                            [client.email],
                        )
                        MailingAttempt.objects.create(mailing=mailing, status='Success')
                    except Exception as e:
                        MailingAttempt.objects.create(mailing=mailing, status='Failure', response=str(e))
