# -*- coding: utf-8 -*-
"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'danubio.menu.CustomMenu'
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu
from pedidos.models import Cliente

class CustomMenu(Menu):
    """
    Custom Menu for danubio admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(u'Início', reverse('admin:index')),
            #items.Bookmarks(),
            items.MenuItem('Clientes','/pedidos/cliente'),
            items.MenuItem('Produtos','/pedidos/produto'),
            items.MenuItem('Pedidos','/pedidos/pedido'),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*',)
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)
