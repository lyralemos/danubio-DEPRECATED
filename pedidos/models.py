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
        HORARIO_CHOICE.append((str(i),'%s:30' % hora))
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
    valor_pago = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    desconto = models.DecimalField(max_digits=5,decimal_places=2,default=0, editable=False)
    observacao = models.TextField(u'Observação',blank=True,null=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICE,default=1,editable=False)
    
    def __unicode__(self):
        return u'Pedido %s' % self.id
    
    def total(self):
        total = 0
        for item in self.pedidoproduto_set.all():
            total += item.valor()
        if self.desconto:
            return total - self.desconto
        return total

    def a_pagar(self):
        resultado = self.total() - self.valor_pago
        if resultado > 0:
            return resultado
        return 0

    def save(self, *args, **kwargs):
        if self.status not in ['2','3'] and self.total() > 0:
            if self.valor_pago < self.total() and self.valor_pago > 0:
                self.status = '4'
            elif self.valor_pago == self.total():
                self.status = '5'
            else:
                self.status = '1'
        super(Pedido,self).save(*args,**kwargs)
    
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