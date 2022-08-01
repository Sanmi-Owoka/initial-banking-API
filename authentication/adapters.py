from django.utils.translation import ugettext_lazy as _
from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpRequest
from django.conf import settings
from django import forms
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from django.core.mail import EmailMessage, EmailMultiAlternatives


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def clean_password(self, password, user=None):
        if len(password) < settings.PASSWORD_MIN_LENGTH:
            raise forms.ValidationError(
                _("Password must be a minimum of {0} " "characters.").format(
                    settings.PASSWORD_MIN_LExNGTH
                )
            )
        return password

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        user.first_name = str(request.POST.get("first_name"))
        user.last_name = str(request.POST.get("last_name"))

        user.save()

        return user

    def render_mail(self, template_prefix, email, context):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        to = [email] if isinstance(email, str) else email
        subject = render_to_string("{0}_subject.txt".format(template_prefix), context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()

        bodies = {}
        for ext in ["html", "txt"]:
            try:
                template_name = "{0}_message.{1}".format(template_prefix, ext)
                bodies[ext] = render_to_string(
                    template_name,
                    context,
                    self.request,
                ).strip()
            except TemplateDoesNotExist:
                if ext == "txt" and not bodies:
                    # We need at least one body
                    raise
        if "txt" in bodies:
            msg = EmailMultiAlternatives(
                subject, bodies["txt"], from_email, to, bcc=settings.BCC_EMAIL
            )
            if "html" in bodies:
                msg.attach_alternative(bodies["html"], "text/html")
        else:
            msg = EmailMessage(
                subject, bodies["html"], from_email, to, bcc=settings.BCC_EMAIL
            )
            msg.content_subtype = "html"  # Main content is now text/html
        return msg

    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)
        msg.send(fail_silently=True)
