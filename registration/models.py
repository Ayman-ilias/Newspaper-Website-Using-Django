from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE

class UserNewsAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    is_editor = models.BooleanField(default=False)
    
    def __str__(self):
        editor_status = "Editor" if self.is_editor else "Viewer"
        return f"{self.user.email} - {editor_status}"
    
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    

    def __str__(self):
        return str(self.user.email)