# Generated by Django 2.2.1 on 2019-05-24 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('lk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True,
                                      verbose_name='Сумма заказа'),
        ),
        migrations.AlterField(
            model_name='productseries',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Цена'),
        ),
        migrations.CreateModel(
            name='PostingGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Кол-во')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена закупки')),
                ('series',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_in_posting',
                                   to='lk.ProductSeries', verbose_name='Серия')),
            ],
            options={
                'verbose_name': 'Поступление товара',
                'verbose_name_plural': 'Поступление товаров',
            },
        ),
    ]