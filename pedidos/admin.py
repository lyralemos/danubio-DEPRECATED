# -*- coding: utf-8 -*-

from django.contrib import admin

from fields import ForeignKeyAdmin

from pedidos.models import Pedido, Produto, Cliente, PedidoProduto

class PedidoProdutoInline(admin.TabularInline):
    extra = 10
    model = PedidoProduto

class PedidoAdmin(ForeignKeyAdmin):
    list_display = ('cliente','data_pedido','data_entrega')
    list_filter = ('data_pedido','data_entrega')
    date_hierarchy = 'data_entrega'
    inlines = (PedidoProdutoInline,)
    related_search_fields = {
        'cliente': ('^nome',),
    }

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome','bairro','telefone')
    list_filter = ('bairro',)

admin.site.register(Pedido,PedidoAdmin)
admin.site.register(Produto)
admin.site.register(Cliente,ClienteAdmin)