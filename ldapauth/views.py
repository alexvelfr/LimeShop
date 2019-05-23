from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from lk.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import SetPhoneForm


# Create your views here.
class AuthView(View):
    def get(self, request):
        ctn = {'form': AuthenticationForm}
        return render(request, 'registration/login.html', context=ctn)

    def post(self, request):
        ctn = {}
        log = request.POST.get('username')
        pwd = request.POST.get('password')
        from django_python3_ldap.auth import ldap
        user = ldap.authenticate(password=pwd, username=log)

        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if not user.phone_number:
                return redirect('setphone')
            else:
                return redirect('/lk')
        else:
            user = User.objects.filter(Q(phone_number=log) | Q(username=log)).first()
            if user and user.check_password(pwd):
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return render(request, 'registration/login.html', context=ctn)


class SetPhone(View):
    def get(self, request):
        ctn = {'form': SetPhoneForm}
        return render(request, 'registration/set_phone.html', context=ctn)

    def post(self, request):
        pass
