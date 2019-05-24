from django.contrib import admin
from django.utils.html import format_html_join

from .models import *


class OrderItemsAdmin(admin.ModelAdmin):
    model = OrderItems
    exclude = ['price']


class OrderAdmin(admin.ModelAdmin):
    model = Order
    fields = ['date', 'user', 'items_in_oreder', 'amount']
    readonly_fields = ('items_in_oreder', 'date', 'amount')

    def items_in_oreder(self, instance):
        obj = instance.order_items.all()
        return format_html_join(
            '',
            '<p>{}, {}шт = {} грн</p>',
            ((c.series, c.count, c.price) for c in obj),
        )


admin.site.site_header = 'Админ панель Lime Shop'
admin.site.site_title = 'Админ панель Lime Shop'
admin.site.index_title = 'Админ панель Lime Shop'

admin.site.register(User)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductSeries)
