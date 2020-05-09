from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from accounts.models import Token
from django.contrib import auth, messages

def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('accounts:login') + f'?token={str(token.uid)}'
    )
    send_mail('Superbeats login link',
              f'Please use this url for login:\n\n{url}',
              'noreply@superbeats',
              [email])
    messages.success(request,
                     'We\'ve sent an email for login. Kindly check your mail for the link.')
    return redirect('/')

def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')