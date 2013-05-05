from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from views import IndexView, SearchListView, SearchPedidosView, CreateClienteView,\
                    UpdateClienteView, CreatePedidoView, UpdatePedidoView, ComprovanteView,\
                    CreateProdutoView, UpdateProdutoView
from models import Cliente, Produto, Pedido

urlpatterns = patterns('',
    url(r'^clientes/add/$', 
        login_required(CreateClienteView.as_view(model=Cliente,success_url='/clientes',template_name='pedidos/form.html')),
        name='add_clientes_view'),
    url(r'^clientes/update/(?P<pk>[\w-]+)/$', 
        login_required(UpdateClienteView.as_view(model=Cliente,success_url='/clientes',template_name='pedidos/form.html')),
        name='update_clientes_view'),
    url(r'^clientes/delete/(?P<pk>[\w-]+)/$',
        login_required(DeleteView.as_view(model=Cliente,success_url='/clientes',template_name='pedidos/confirm_delete.html')),
        name='delete_clientes_view'),
    url(r'^clientes/$', 
        login_required(SearchListView.as_view(model=Cliente,template_name='pedidos/cliente_list.html')),
        name='clientes_view'),

    url(r'^produtos/add/$', 
        login_required(CreateProdutoView.as_view()),
        name='add_produtos_view'),
    url(r'^produtos/update/(?P<pk>[\w-]+)/$', 
        login_required(UpdateProdutoView.as_view()),
        name='update_produtos_view'),
    url(r'^produtos/delete/(?P<pk>[\w-]+)/$', 
        login_required(DeleteView.as_view(model=Produto,success_url='/produtos',template_name='pedidos/confirm_delete.html')),
        name='delete_produtos_view'),
    url(r'^produtos/$', 
        login_required(SearchListView.as_view(model=Produto,template_name='pedidos/produto_list.html')),
        name='produtos_view'),

    url(r'^pedidos/add/$', 
        login_required(CreatePedidoView.as_view(model=Pedido,success_url='/pedidos',template_name='pedidos/pedido.html')),
        name='add_pedidos_view'),
    url(r'^pedidos/update/(?P<pk>[\w-]+)/$', 
        login_required(UpdatePedidoView.as_view(model=Pedido,success_url='/pedidos',template_name='pedidos/pedido.html')),
        name='update_pedidos_view'),
    url(r'^pedidos/delete/(?P<pk>[\w-]+)/$', 
        login_required(DeleteView.as_view(model=Pedido,success_url='/pedidos',template_name='pedidos/confirm_delete.html')),
        name='delete_pedidos_view'),
    url(r'^pedidos/imprimir/(?P<pk>[\w-]+)/$', 
        login_required(ComprovanteView.as_view(model=Pedido)),
        name='imprimir_pedido_view'),
    url(r'^pedidos/$',
        login_required(SearchPedidosView.as_view(model=Pedido,template_name='pedidos/pedidos_list.html')),
        name='pedidos_view'),

    #AJAX views
    url(r'^pedidos/get_endereco/(?P<pk>[\w-]+)/$','pedidos.views.get_endereco',name='get_endereco'),
    url(r'^pedidos/get_price/(?P<pk>[\w-]+)/$','pedidos.views.get_price',name='get_price'),
    url(r'^pedidos/modificar_status/(?P<pk>[\w-]+)/$','pedidos.views.modificar_status',name='modificar_status'),

    url(r'^$', login_required(IndexView.as_view()),name='index'),
)