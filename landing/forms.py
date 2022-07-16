from django import forms
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from watchdog.telegram import log
from .models import Contact


class ContactForm(forms.Form):
    """
    The contact Form
    """
    name = forms.CharField(required=True, label=_("Name"))
    email = forms.EmailField(required=True, label=_("Email"))
    subject = forms.CharField(required=False, label=_("Subject"))
    message = forms.CharField(required=True, label=_("Message"), widget=forms.Textarea)

    captcha = ReCaptchaField(required=False,  widget=ReCaptchaV2Checkbox(
        attrs={'data-theme': 'dark'}), label=_("Captcha"))

    def save(self):
        """
        Save to database and Notice to the Watchdog
        :return:
        """
        c = Contact()
        c.name = self.cleaned_data['name']
        c.email = self.cleaned_data['email']
        c.subject = self.cleaned_data['subject']
        c.message = self.cleaned_data['message']
        c.save()
        print("Saved to database")
        log("New Contact: " + c.name + " " + c.email + " " + c.subject + " " + c.message)
