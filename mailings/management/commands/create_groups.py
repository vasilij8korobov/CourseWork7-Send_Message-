from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailings.models import Client, Message, Mailing


class Command(BaseCommand):
    help = 'Create default groups'

    def handle(self, *args, **kwargs):
        manager_group, created = Group.objects.get_or_create(name='Managers')

        client_content_type = ContentType.objects.get_for_model(Client)
        message_content_type = ContentType.objects.get_for_model(Message)
        mailing_content_type = ContentType.objects.get_for_model(Mailing)

        client_permissions = Permission.objects.filter(content_type=client_content_type, codename='view_client_custom')
        message_permissions = Permission.objects.filter(content_type=message_content_type,
                                                        codename='view_message_custom')
        mailing_permissions = Permission.objects.filter(content_type=mailing_content_type,
                                                        codename='view_mailing_custom')

        manager_group.permissions.add(*client_permissions, *message_permissions, *mailing_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created default groups'))
