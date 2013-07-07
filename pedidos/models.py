# -*- coding: utf-8 -*-
from datetime import datetime

from djutils.decorators import memoize

from django.db import models
from django.dispatch import receiver

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
    ('3','Não entregue'),
    ('4','Pago Parcialmente'),
    ('5','Pago'),
)


def get_horarios():
    HORARIO_CHOICE = []
    i = 0
    for hora in range(8,18):
        HORARIO_CHOICE.append((str(i),'%s:00' % hora))
        i += 1
    HORARIO_CHOICE.append((str(i),'18:00'))
    return HORARIO_CHOICE

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente)
    endereco = models.ForeignKey(Endereco)
    itens = models.ManyToManyField(Produto,through='PedidoProduto',editable=False)
    data_pedido = models.DateTimeField(auto_now_add=True)
    data_entrega = models.DateField()
    hora_entrega = models.CharField(max_length=10,choices=get_horarios())
    entrega = models.BooleanField()
    valor_pago = models.DecimalField(max_digits=5,decimal_places=2,default=0, null=True, blank=True)
    desconto = models.DecimalField(max_digits=5,decimal_places=2,default=0, editable=False)
    observacao = models.TextField(u'Observação',blank=True,null=True)
    entregue = models.BooleanField(editable=False)
    
    def __unicode__(self):
        return u'Pedido %s' % self.id
    
    def total(self):
        total = 0
        query = '''
        select sum(quantidade*preco) 
            from pedidos_pedidoproduto, pedidos_produto 
            where pedidos_pedidoproduto.produto_id = pedidos_produto.id and 
                pedidos_pedidoproduto.pedido_id = %s
        '''

        from django.db import connection, transaction
        cursor = connection.cursor()

        cursor.execute(query, [self.id])
        total = cursor.fetchone()[0]

        if self.desconto:
            return total - self.desconto
        return total

    def a_pagar(self):
        resultado = self.total() - self.valor_pago
        if resultado > 0:
            return resultado
        return 0

    @memoize
    def status(self):
        if self.entregue:
            return 2
        elif datetime.today().date() > self.data_entrega:
            return 3
        else:
            if self.valor_pago < self.total() and self.valor_pago > 0:
                return 4
            elif self.valor_pago == self.total():
                return 5
            else:
                return 1

    def get_status_display(self):
        return dict(STATUS_CHOICE)[str(self.status())]

    
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