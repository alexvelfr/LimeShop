from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from lk.models import User
from django_python3_ldap.auth import ldap
from .forms import SetPhoneForm
import os


# Create your views here.
class AuthView(View):
    def get(self, request, *args, **kwargs):
        ctn = {}
        if 'logout' in request.path:
            logout(request)
            return redirect('/auth')
        return render(request, 'registration/login.html', context=ctn)

    def post(self, request):
        ctn = {}
        log = request.POST.get('username').replace(f'@{os.environ.get("DOMAIN")}', '')
        pwd = request.POST.get('password')
        user = ldap.authenticate(password=pwd, username=log)
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            user = User.objects.filter(Q(phone_number=log) | Q(username=log)).first()
            if user and user.check_password(pwd):
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        if request.user.is_authenticated:
            if not user.phone_number:
                return redirect('set_phone')
            else:
                return redirect('/')
        else:
            ctn['errors'] = 'Неверные лоин или пароль'
        return render(request, 'registration/login.html', context=ctn)


class SetPhone(View):
    def get(self, request):
        form = SetPhoneForm(user=request.user)
        if request.user.is_authenticated and request.user.phone_number:
            form.initial = {'phone_number': request.user.phone_number}
        return render(request, 'registration/set_phone.html', context={'form': form})

    def post(self, request):
        form = SetPhoneForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            user.phone_number = form.cleaned_data.get('phone_number')
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
        return render(request, 'registration/set_phone.html', context={'form': form})
