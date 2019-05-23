from django.contrib.auth.decorators import login_required
from django.urls import path
from ldapauth.views import AuthView, SetPhone


urlpatterns = [
    path('', AuthView.as_view(), name='auth_url'),
    path('?<logout: str>', AuthView.as_view(), name='auth_url'),
    path('setphone/', login_required(SetPhone.as_view()), name='set_phone')
]
