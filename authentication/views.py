from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignupForm, TestForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import generate_token
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth.views import LoginView    

# Create your views here.


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            # message = render_to_string('acc_active_email.html', {  
            message = render_to_string('activate.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':generate_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please go to your email and confirm your email address by click activation link from email to complete the registration')  
    else:  
        form = SignupForm()  
    return render(request, 'signup.html', {'form': form}) 

class activate(View):
    def get(self, request,uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
           # messages.add_message(request, messages.INFO,'account activated sucesfully')
            return redirect ('authentication:login') #change to login 
        return render(request,'activate_failed.html', status=401) 
    



class Login(LoginView):
    template_name = 'login.html'

def signin(request):
    return render(request, 'signin.html')

def user_logout(request):
    logout(request)
    return redirect('/')

