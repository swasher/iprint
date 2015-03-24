from django.db import models
from rept.models import Manufacturer


class Doska(models.Model):
    articul = models.CharField(max_length=20, unique=True, verbose_name='Артикул')
    make_date = models.DateField(blank=True, null=True, verbose_name='Дата изг.')
    name = models.CharField(max_length=100, verbose_name='Наименование')
    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Изготовитель')
    price = models.DecimalField(blank=True, max_digits=12, decimal_places=2, null=True, verbose_name='Стоимость, уе.')
    description = models.TextField(blank=True, verbose_name='Описание')
    maintenance = models.TextField(blank=True, verbose_name='Обслуживание', help_text='Тут должны быть описаны любые работы, проведенные с доской.')
    customer = models.TextField(blank=True, verbose_name='Заказчик', help_text='Кто платил за доску или типичный заказчик.')
    spusk = models.ImageField(blank=True, null=True, upload_to='spusk', verbose_name='Спуск', help_text='Изображение печатного листа')
    doska = models.ImageField(blank=True, null=True, upload_to='doska', verbose_name='Доска', help_text='Изображение доски')

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    def __str__(self):
        return '[{}] {}'.format(self.articul, self.name)


class Knife(models.Model):
    doska = models.ForeignKey(Doska)
    name = models.CharField(max_length=50)
    razvertka_w = models.PositiveSmallIntegerField(blank=True, null=True)
    razvertka_h = models.PositiveSmallIntegerField(blank=True, null=True)
    gabarit_a = models.PositiveSmallIntegerField(blank=True, null=True)
    gabarit_b = models.PositiveSmallIntegerField(blank=True, null=True)
    gabarit_c = models.PositiveSmallIntegerField(blank=True, null=True)
    knife = models.ImageField(blank=True, null=True, upload_to='knife', verbose_name='Нож, изобр.', help_text='Изображение ножа')
    drawing = models.FileField(blank=True, null=True, upload_to='drawing', verbose_name='Чертеж, PDF', help_text='Файл чертежа (PDF)')

    class Meta:
        verbose_name = 'Штанц'
        verbose_name_plural = 'Штанцы'

    def __str__(self):
        return '{}'.format(self.name)
