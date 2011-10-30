# -*- coding: utf-8 -*-
from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200,null=True,blank=True)
    telefone = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.nome
    
    def getAutocomplete(self):
        return '%s <br /> <small>%s</small>' % (self.nome,self.endereco)
    
    class Meta():
        ordering = ('nome',)

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.nome
    
    class Meta():
        ordering = ('nome',)

STATUS_CHOICE = (
    (1,'Aberto'),
    (2,'Entregue'),
)

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente)
    itens = models.ManyToManyField(Produto,through='PedidoProduto')
    data_pedido = models.DateTimeField(auto_now_add=True)
    data_entrega = models.DateTimeField()
    observacao = models.TextField(u'Observação',blank=True,null=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICE,editable=False)
    pago = models.BooleanField(editable=False)
    
    def __unicode__(self):
        return u'Pedido %s' % self.id
    
    class Meta():
        ordering = ('-data_entrega',)
        
    
class PedidoProduto(models.Model):
    pedido = models.ForeignKey(Pedido)
    produto = models.ForeignKey(Produto)
    quantidade = models.IntegerField()
    
    def __unicode__(self):
        return '%s' % self.id
    
    class Meta():
        verbose_name = u'Ítem'