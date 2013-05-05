from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView
from django.db.models import Q

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet

from models import Cliente,Endereco,Produto,Pedido,PedidoProduto
from forms import PedidoForm, PedidoProdutoForm, ProdutoForm

class IndexView(TemplateView):

	template_name = "pedidos/index.html"

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['cliente_list'] = Cliente.objects.all()[:5]
		context['produto_list'] = Produto.objects.all()[:5]
		context['pedido_list'] = Pedido.objects.all()[:5]
		return context

class SearchListView(ListView):

	def get_queryset(self):
		search = self.request.GET.get('search',None)
		if search:
			return self.model.objects.filter(nome__contains=search)
		return self.model.objects.all()

class SearchPedidosView(ListView):

	def get_queryset(self):
		termo = self.request.GET.get('q',None)
		status = self.request.GET.get('status',None)
		order = self.request.GET.get('order',None)

		search = self.model.objects.all()

		if termo:
			search = search.filter(Q(cliente__nome__contains=termo) | Q(pk__contains=termo))
		if status:
			search = search.filter(status=status)
		if order:
			search = search.order_by(order) 
		return search

class EnderecoInline(InlineFormSet):
    model = Endereco

class CreateClienteView(CreateWithInlinesView):
    model = Cliente
    inlines = [EnderecoInline]

class UpdateClienteView(UpdateWithInlinesView):
    model = Cliente
    inlines = [EnderecoInline]

class PedidoProdutoInline(InlineFormSet):
	model = PedidoProduto
	form_class = PedidoProdutoForm
	extra = 10

class CreatePedidoView(CreateWithInlinesView):
	model = Pedido
	form_class = PedidoForm
	inlines = [PedidoProdutoInline]

class UpdatePedidoView(UpdateWithInlinesView):
	model = Pedido
	form_class = PedidoForm
	inlines = [PedidoProdutoInline]

class CreateProdutoView(CreateView):
	model = Produto
	form_class = ProdutoForm
	success_url='/produtos'
	template_name='pedidos/form.html'

class UpdateProdutoView(UpdateView):
	model = Produto
	form_class = ProdutoForm
	success_url='/produtos'
	template_name='pedidos/form.html'

class ComprovanteView(DetailView):

	template_name='pedidos/comprovante.html'

	def get_context_data(self,*args, **kwargs):
		context = super(ComprovanteView, self).get_context_data(*args,**kwargs)
		context['itens_pedido'] = PedidoProduto.objects.filter(pedido__pk=self.kwargs['pk'])
		context['repeat'] = range(2)
		return context

def get_price(request,pk):
	produto = Produto.objects.get(pk=pk)
	results = simplejson.dumps(
        {
            'pk': produto.pk,
            'price': float(produto.preco)
        }
    )
	return HttpResponse(results, mimetype='application/javascript')

def get_endereco(request,pk):
	enderecos = Endereco.objects.filter(cliente__pk=pk)
	results = simplejson.dumps([
		{
			'pk' : endereco.pk,
			'nome' : endereco.__unicode__()
		} for endereco in enderecos
	])
	return HttpResponse(results, mimetype='application/javascript')

def modificar_status(request,pk):
	pedido = Pedido.objects.get(pk=pk)
	acao = request.GET.get('acao')
	if acao == '5':
		pedido.valor_pago = pedido.total()
	pedido.status = acao
	pedido.save()
	return HttpResponseRedirect(reverse('pedidos_view'))

def imprimir(request,pk):
	return HttpResponse()