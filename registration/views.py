from typing import Any
from django.shortcuts import render, redirect
from .import forms
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
# from .tokens import account_activation_token
# from django.utils.encoding import force_bytes, force_text
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.http import HttpResponse
from .tokens import generate_token




def send_email(user,subject, template):
    message = render_to_string(template, {
        'user' : user,
        })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


def send_reg_email(user,subject,domain,uid,token,template):
    message = render_to_string(template, {
        'user' : user,
        'domain' : domain,
        'uid': uid,
        'token': token
        })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()
    print("registration Email sent successfully")




# def register(request):
#     if request.method == 'POST':
#         register_form = forms.RegistrationForm(request.POST)
#         if register_form.is_valid():
#             user = register_form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             domain=current_site.domain,
#             # uid=urlsafe_base64_encode(force_bytes(user.pk)).decode(),
#             uid = urlsafe_base64_encode(force_bytes(user.pk)),
#             token = account_activation_token.make_token(user),
#             send_reg_email(user, 'Registration Successful',domain,uid,token,'registration_email.html')
#             messages.success(request, 'Registered Successfully ツ')
#             return redirect('profile')
#     else:
#         register_form = forms.RegistrationForm()

#     return render(request, 'user_registration.html', {'form': register_form})


@login_required
def profile(request):
    return render(request, 'profile.html')



# class UserLoginView(LoginView):
#     template_name='user_login.html'
#     # success_url=reverse_lazy('home')

#     def get_success_url(self):
#         activation_link = reverse_lazy('activate', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(self.request.user.pk)), 'token': account_activation_token.make_token(self.request.user)})
#         return activation_link
    

#     def form_valid(self, form):
#         messages.success(self.request,'Logged In Successfully ツ ')
#         return super().form_valid(form)
    
#     def form_invalid(self, form):
#         messages.success(self.request,' Invalid Information ( ˘︹˘ ) ')
#         return super().form_invalid(form)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['type'] = 'Login'
#         return context    
    
class UserLoginView(LoginView):
    template_name='user_login.html'
    # success_url=reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('home')
    

    def form_valid(self, form):
        messages.success(self.request,'Logged In Successfully ツ ')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request,' Invalid Information ( ˘︹˘ ) ')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context    


# def form_valid(self, form):
#         messages.success(self.request,'Logged In Successfully ツ ')
#         return super().form_valid(form)

# def get_success_url(self):
#         activation_link = reverse_lazy('activate', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(self.request.user.pk)), 'token': account_activation_token.make_token(self.request.user)})
#         return activation_link


    
@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeuserForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated successfully')
            return redirect('edit_profile')
    else:
        profile_form = forms.ChangeuserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': profile_form})

def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'PassWord Updated Successfully ツ')
            send_email(request.user, "PassWord Change", "pass_change_email.html")
            update_session_auth_hash(request,form.user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'pass_change.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request,"Logged out successfully ツ")
    return redirect('user_login')
    

def test(request):
    return render(request,'register.html')








def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=True)
            user.is_active = False
            user.save()
            

            
            current_site = get_current_site(request)
            domain = current_site.domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = generate_token.make_token(user)
            subject = "Confirm Your Email Address"

            send_reg_email(user, subject, domain, uid, token, 'registration_email.html')
            messages.success(request, 'Registered Successfully ツ Please check your email to confirm your email address.')
            return redirect('user_registration')  

    else:
        register_form = forms.RegistrationForm()

    return render(request, 'user_registration.html', {'form': register_form})



def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user,token):
        user.is_active = True

       
        user.save()
        login(request,user)
        messages.success(request, "Your Account has been activated!!....Please Login Now!!")
        # messages.success(request, "Please Login Now!!")
        return redirect('user_login')
    else:
        return redirect('user_login')
    


