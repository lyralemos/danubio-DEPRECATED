# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin

from ajax_select import make_ajax_form,make_ajax_field
from ajax_select.admin import AjaxSelectAdmin

from pedidos.models import Pedido, Produto, Cliente, PedidoProduto

class PedidoProdutoAdminForm(forms.ModelForm):
    produto = make_ajax_field(PedidoProduto,'produto','produto',help_text=' ')
    class Meta:
        model = PedidoProduto

class PedidoProdutoInline(admin.TabularInline):
    extra = 10
    model = PedidoProduto
    form = PedidoProdutoAdminForm
    #form = make_ajax_form(PedidoProduto,dict(produto='produto'))

class PedidoAdminForm(forms.ModelForm):
    cliente = make_ajax_field(Pedido,'cliente','cliente',help_text=' ')

    class Meta:
        model = Pedido

class PedidoAdmin(AjaxSelectAdmin):
    #form = make_ajax_form(Pedido,dict(cliente='cliente'))
    form = PedidoAdminForm
    list_display = ('id','cliente','total','pago','data_entrega','status')
    list_filter = ('data_entrega','status')
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