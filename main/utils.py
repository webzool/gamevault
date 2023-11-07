from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage

from django.http import HttpResponse, StreamingHttpResponse
import csv
import pytz


def send_mail(name, user_mail, subject, message):
    from_email = settings.EMAIL_HOST_USER
    recipient = user_mail
    subject = subject
    context = {
        'name': name,
        'body': message,
    }
    body = render_to_string('emails/contact.html', context)
    mail = EmailMessage(subject, body=body, from_email=from_email, to=[recipient,])
    mail.content_subtype = 'html'
    mail.send(fail_silently=True)


def export_to_csv(self, request, queryset):

    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        obj.created_at = obj.created_at.astimezone(pytz.timezone('America/Los_Angeles')).strftime('%m-%d-%y %H:%M')
        writer.writerow([getattr(obj, field) for field in field_names])
    return response