# -*- coding: utf-8 -*-

from django import forms

from pedidos.models import Pedido, Produto, Cliente, PedidoProduto, Endereco

class PedidoForm(forms.ModelForm):
    endereco = forms.ModelChoiceField(queryset=Endereco.objects.all())
    valor_pago = forms.DecimalField(max_digits=5,decimal_places=2,localize=True,required=False,initial=0)


    def __init__(self, list=None, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Pedido
        exclude = ('status',)

class PedidoProdutoForm(forms.ModelForm):
    
    class Meta:
        model = PedidoProduto

class ProdutoForm(forms.ModelForm):
    preco = forms.DecimalField(max_digits=5,decimal_places=2,localize=True)

    class Meta:
        model = Produto