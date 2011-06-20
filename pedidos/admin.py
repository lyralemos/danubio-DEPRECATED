# -*- coding: utf-8 -*-

from django.contrib import admin

from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

from pedidos.models import Pedido, Produto, Cliente, PedidoProduto

class PedidoProdutoInline(admin.TabularInline):
    extra = 10
    model = PedidoProduto
    form = make_ajax_form(PedidoProduto,dict(produto='produto'))

class PedidoAdmin(AjaxSelectAdmin):
    form = make_ajax_form(Pedido,dict(cliente='cliente'))
    list_display = ('cliente','data_pedido','data_entrega')
    list_filter = ('data_pedido','data_entrega')
    date_hierarchy = 'data_entrega'
    inlines = (PedidoProdutoInline,)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome','bairro','telefone')
    list_filter = ('bairro',)

admin.site.register(Pedido,PedidoAdmin)
admin.site.register(Produto)
admin.site.register(Cliente,ClienteAdmin)