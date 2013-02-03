# -*- coding: utf-8 -*-
from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    telefone1 = models.CharField('Telefone',max_length=20)
    telefone2 = models.CharField('Telefone',max_length=20,null=True,blank=True)
    
    def __unicode__(self):
        return self.nome
    
    class Meta():
        ordering = ('nome',)
        verbose_name = u'Cliente'

class Endereco(models.Model):
    rua = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200,null=True,blank=True)
    cliente = models.ForeignKey(Cliente)

    def __unicode__(self):
        return '%s - %s' % (self.rua, self.bairro)

    class Meta():
        verbose_name = u'Endereço'

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=5,decimal_places=2)
    
    def __unicode__(self):
        return self.nome
    
    class Meta():
        ordering = ('nome',)

STATUS_CHOICE = (
    ('1','Aberto'),
    ('2','Entregue'),
    ('3','Cancelado'),
)

HORARIO_CHOICE = []
i = 0
for hora in range(8,18):
    HORARIO_CHOICE.append((str(i),'%s:00' % hora))
    i += 1
    HORARIO_CHOICE.append((str(i),'%s:30' % hora))
    i += 1
HORARIO_CHOICE.append((str(i),'18:00'))

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente)
    endereco = models.ForeignKey(Endereco)
    itens = models.ManyToManyField(Produto,through='PedidoProduto',editable=False)
    data_pedido = models.DateTimeField(auto_now_add=True)
    data_entrega = models.DateField()
    hora_entrega = models.CharField(max_length=10,choices=HORARIO_CHOICE)
    entrega = models.BooleanField()
    observacao = models.TextField(u'Observação',blank=True,null=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default=1)
    
    def __unicode__(self):
        return u'Pedido %s' % self.id
    
    def pago(self):
        return self.total() == 0.0 or self.status == '2'
    pago.boolean = True
    
    def total(self):
        total = 0
        for item in self.pedidoproduto_set.all():
            total += item.valor()
        return ('R$ %0.02f' % (total)).replace('.',',')
    
    class Meta():
        ordering = ('-data_entrega',)
        
    
class PedidoProduto(models.Model):
    pedido = models.ForeignKey(Pedido)
    produto = models.ForeignKey(Produto)
    quantidade = models.IntegerField(default=0)
    
    def __unicode__(self):
        return '%s' % self.id
    
    def valor(self):
        return self.produto.preco*self.quantidade
    
    class Meta():
        verbose_name = u'Ítem'