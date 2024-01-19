from django.contrib import admin
from .models import UserNewsAccount,UserInfo
# from .views import send_email
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string



def send_email(user,subject, template):
    message = render_to_string(template, {
        'user' : user,
        })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

class UserNewsAccountAdmin(admin.ModelAdmin):
    list_display = ['user','is_editor']

    def save_model(self, request, obj, form, change):
        obj.save()
        send_email(obj.user,"Loan Approval", "editor_email.html")
        super().save_model(request, obj, form, change)

admin.site.register(UserNewsAccount, UserNewsAccountAdmin)
admin.site.register(UserInfo)