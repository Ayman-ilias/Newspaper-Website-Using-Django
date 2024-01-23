from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import  GENDER_TYPE,UserNewsAccount,UserInfo

class RegistrationForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    country = forms.CharField(max_length=100)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    city = forms.CharField(max_length= 100)
    mobile_number = forms.DecimalField(max_digits=12, decimal_places=2)
    
    

    class Meta:
        model = User
        fields = ['username' ,'first_name' , 'last_name','email', 'password1','password2', 'gender', 'birth_date','mobile_number','city','country']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit:
            our_user.save()
            gender = self.cleaned_data.get('gender')
            country = self.cleaned_data.get('country')
            birth_date = self.cleaned_data.get('birth_date')
            city = self.cleaned_data.get('city')

            UserInfo.objects.create(
                user=our_user,
                country=country,
                city=city,
            )
            UserNewsAccount.objects.create(
                user=our_user,
                gender=gender,
                birth_date=birth_date,
            )
        return our_user




class ChangeuserForm(UserChangeForm):
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    mobile_number = forms.DecimalField(max_digits=12, decimal_places=2)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    password= None


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'birth_date', 'mobile_number', 'city', 'country']
        exclude = ['password']

    def __init__(self, *args, **kwargs):
        super(ChangeuserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].help_text = None