from django.shortcuts import render
from django.views.generic import View
# Create your views here.


class IndexView(View):

    def get(self, request):
        return render(request, template_name='lk/index.html', context={'title': 'Dashboard'})
