from django.urls import path
from ldapauth.views import AuthView, SetPhone


urlpatterns = [
    path('', AuthView.as_view(), name='auth_url'),
    path('setphone/', SetPhone.as_view(), name='set_phone')
]
