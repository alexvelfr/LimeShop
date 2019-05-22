from django.shortcuts import render
from django.views.generic import View
# Create your views here.


class HomeView(View):

    def get(self, request):
        return render(request, template_name='landing/index.html', context={'title': 'Home page'})
