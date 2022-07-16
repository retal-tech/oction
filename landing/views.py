"""
Landing View, Error Views
"""
from django.shortcuts import render
from django.views.generic import FormView

from watchdog.telegram import log
from .models import Projects
from .forms import ContactForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class LandingView(FormView):
    """
    Landing View, using template from trt/templates
    """
    template_name = "landing/landing.html"
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        """
        Make an dictionary of data
        """
        context = super().get_context_data()
        context['portfolio'] = Projects.objects.all()
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the data
        """
        print("Form is valid")
        form.save()
        # Send Success Message to the client
        messages.success(self.request, _("Your message has been sent!"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, return the form
        """
        print("Form is invalid")
        print(form.errors)
        return super().form_invalid(form)


def handler500(request, *args, **argv):
    """
    500 handler, called from main `url.py`
    """
    log(f"""
        ERROR 500! (500)
        path: {request.path}
        method: {request.method}
        user: {request.user}
        HTTP_USER_AGENT: {request.META.get('HTTP_USER_AGENT')}
        HTTP_REFERER: {request.META.get('HTTP_REFERER')}
        HTTP_ACCEPT_LANGUAGE: {request.META.get('HTTP_ACCEPT_LANGUAGE')}
        HTTP_ACCEPT_ENCODING: {request.META.get('HTTP_ACCEPT_ENCODING')}
        HTTP_ACCEPT: {request.META.get('HTTP_ACCEPT')}
        HTTP_CONNECTION: {request.META.get('HTTP_CONNECTION')}
        HTTP_HOST: {request.META.get('HTTP_HOST')}
    """)
    response = render(request, template_name='errors/500.html', context={})
    response.status_code = 500
    return response


def handler404(request, *args, **argv):
    """
    404 handler, called from main `url.py`
    """
    response = render(request, template_name='errors/404.html', context={})
    response.status_code = 404
    return response
