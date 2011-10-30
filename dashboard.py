# -*- coding: utf-8 -*-
"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'danubio.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'danubio.dashboard.CustomAppIndexDashboard'
"""
from datetime import date

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

from pedidos.models import Pedido


class EncomendasModule(modules.DashboardModule):
    title = 'Encomendas'
    template = 'pedidos/encomendas.html'

    def init_with_context(self, context):
        self.total = Pedido.objects.filter(data_entrega__startswith=date.today()).count()
        
    def is_empty(self):
        return False

class RelatorioModule(modules.DashboardModule):
    title = u'Relatórios'
    template = 'pedidos/relatorios.html'

    def is_empty(self):
        return False

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for danubio.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        self.children.append(modules.ModelList(
            'Pedidos', ['pedidos.*',]
        ))
        
        self.children.append(modules.ModelList(
            u'Administração', ['django.contrib.auth.*',]
        ))
        
        self.children.append(EncomendasModule())
        self.children.append(RelatorioModule())
        '''
        self.children.append(modules.LinkList(
            u'Relatórios',
            draggable=True,
            deletable=False,
            collapsible=True,
            children=[
                [u'Encomendas por dia', '/'],
                [u'Encomendas por período',reverse('%s:password_change' % site_name)],
            ]
        ))
        '''

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))



class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for danubio.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
