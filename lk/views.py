from django.shortcuts import render
from django.views.generic import View
from .models import *
# Create your views here.


class IndexView(View):

    def get(self, request):
        return render(request, template_name='lk/index.html', context={'title': 'Личный кабинет Lime Shop'})

    def post(self, request):
        ctx = {'title': 'Личный кабинет Lime Shop'}
        try:
            prod_code = int(request.POST.get('product_code'))
            count = int(request.POST.get('count'))
        except:
            return render(request, template_name='lk/index.html', context=ctx)
        prod_series = ProductSeries.objects.filter(number=prod_code).first()
        if not prod_series:
            ctx['error'] = 'Товар не найден в базе. Проверьте правильность ввода'
            return render(request, template_name='lk/index.html', context=ctx)
        elif prod_series.count < count:
            ctx['error'] = 'На складе недостаточно товара. Проверьте правильность ввода'
            return render(request, template_name='lk/index.html', context=ctx)
        order = Order(user=request.user)
        order.save()
        OrderItems(order=order, series=prod_series, count=count).save()
        ctx['success'] = True
        return render(request, template_name='lk/index.html', context=ctx)


class HistoryView(View):

    def get(self, request):
        query = OrderItems.objects.filter(order__user=request.user, order__amount__isnull=False).order_by('-order__date')
        total_amount = query.aggregate(Sum('price')).get('price__sum') or 0
        items = query.all()
        return render(request, template_name='lk/history_order.html', context={
            'title': 'История покупок Lime',
            'items': items,
            'total_amount': total_amount
        })


class ReportView(View):

    def get(self, request):
        return render(request, template_name='lk/report.html', context={
            'title': 'Отчеты Lime Shop',
        })
