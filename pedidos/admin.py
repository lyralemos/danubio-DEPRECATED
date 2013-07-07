# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin

from pedidos.models import Pedido, Produto, Cliente, PedidoProduto


class PedidoProdutoInline(admin.TabularInline):
    extra = 10
    model = PedidoProduto

class PedidoAdminForm(forms.ModelForm):

    class Meta:
        model = Pedido

class PedidoAdmin(admin.ModelAdmin):
    form = PedidoAdminForm
    list_display = ('id','cliente','total','data_entrega','status')
    list_filter = ('data_entrega',)
    date_hierarchy = 'data_entrega'
    search_fields = ('cliente__nome','id')
    inlines = (PedidoProdutoInline,)

    class Media:
        js = ('js/jquery.meio.mask.js','js/functions.js')

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome','telefone1','telefone2')

admin.site.register(Pedido,PedidoAdmin)
admin.site.register(Produto)
admin.site.register(Cliente,ClienteAdmin)