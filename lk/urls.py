from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import IndexView, HistoryView, ReportView

urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index'),
    path('history/', login_required(HistoryView.as_view()), name='history'),
    path('reports/', login_required(ReportView.as_view()), name='reports'),
]
