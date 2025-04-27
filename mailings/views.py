from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm


# Home views
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cache_key = 'home_data'
    cached_data = cache.get(cache_key)

    if not cached_data:
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status='Started').count()
        unique_clients = Client.objects.count()
        mailings = Mailing.objects.all()

        cached_data = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_clients': unique_clients,
            'mailings': mailings,
        }
        cache.set(cache_key, cached_data, timeout=60*15)

    return render(request, 'mailings/home.html', cached_data)


# Client views
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailings/client_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        cache_key = 'client_list'
        cached_data = cache.get(cache_key)
        if not cached_data:
            cached_data = list(queryset)
            cache.set(cache_key, cached_data, timeout=60*15)
        return cached_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('client_list')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailings/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailings/client_detail.html'
    context_object_name = 'client'


# Message views
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailings/message_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        cache_key = 'message_list'
        cached_data = cache.get(cache_key)
        if not cached_data:
            cached_data = list(queryset)
            cache.set(cache_key, cached_data, timeout=60*15)
        return cached_data


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('message_list')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'
    context_object_name = 'message'


# Mailing views
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        cache_key = 'mailing_list'
        cached_data = cache.get(cache_key)
        if not cached_data:
            cached_data = list(queryset)
            cache.set(cache_key, cached_data, timeout=60*15)
        return cached_data


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing_list')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'


# MailingAttempt views
class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailings/mailingattempt_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        cache_key = 'mailingattempt_list'
        cached_data = cache.get(cache_key)
        if not cached_data:
            cached_data = list(queryset)
            cache.set(cache_key, cached_data, timeout=60*15)
        return cached_data


def statistics(request):
    cache_key = 'statistics_data'
    cached_data = cache.get(cache_key)

    if not cached_data:
        attempts = MailingAttempt.objects.all()
        cached_data = {
            'total_attempts': attempts.count(),
            'successful_attempts': attempts.filter(status='Success').count(),
            'failed_attempts': attempts.filter(status='Failure').count(),
        }
        cache.set(cache_key, cached_data, timeout=60*15)

    return render(request, 'mailings/statistics.html', cached_data)
