# -*- coding: utf-8 -*-

from django import forms

from ajax_select import make_ajax_form,make_ajax_field

from pedidos.models import Pedido, Produto, Cliente, PedidoProduto, Endereco, HORARIO_CHOICE

class PedidoForm(forms.ModelForm):
    cliente = make_ajax_field(Pedido,'cliente','cliente',help_text=' ')
    endereco = forms.ModelChoiceField(queryset=Endereco.objects.all())

    def __init__(self, list=None, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        

    class Meta:
        model = Pedido
        exclude = ('status',)

class PedidoProdutoForm(forms.ModelForm):
    produto = make_ajax_field(PedidoProduto,'produto','produto',help_text=' ')
    
    class Meta:
        model = PedidoProduto