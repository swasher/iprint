from django import forms
from django.contrib import admin
from stanzforms.models import Doska, Knife
from rept.models import Manufacturer


class KnifeAdminInLine(admin.TabularInline):
    model = Knife
    extra = 0
    list_display = ('doska', 'name', 'razvertka_w', 'razvertka_h', 'gabarit_a', 'gabarit_b', 'gabarit_c', 'knife', 'drawing')


class DoskaAdminForm(forms.ModelForm):
    class Meta:
        model = Doska
        fields = ['make_date', 'articul', 'name', 'manufacturer', 'price', 'description', 'maintenance', 'customer', 'spusk', 'doska']

    def __init__(self, *args, **kwargs):
        """
        Суть этого метода в том, что в инлайне "Технологические операции" в поле "Печатный лист" выводятся только
        принадлежащие к текущему заказу печатные листы. Иначе Джанго пофиг на них - вываливает всю существующие printingsheet's
        """
        super(DoskaAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['manufacturer'].queryset = Manufacturer.objects.filter(produce='sta')


class DoskaAdmin(admin.ModelAdmin):
    save_as = True

    # В форме редактирование возле "плюсика" появляется "карандашик" (Django 1.8)
    show_change_link = True

    form = DoskaAdminForm

    inlines = [KnifeAdminInLine]

admin.site.register(Doska, DoskaAdmin)