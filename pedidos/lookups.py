from pedidos.models import Cliente
from django.db.models import Q

class ClienteLookup(object):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        #return Cliente.objects.filter(Q(nome__istartswith=q) | Q(nome__istartswith=q) | Q(nome__istartswith=q))
        return Cliente.objects.filter(nome__contains=q)

    def format_result(self,cliente):
        """ the search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """
        return u"<b>%s</b> <br />%s - %s<br /> (%s)" % (cliente.nome, cliente.endereco,cliente.bairro,cliente.telefone)

    def format_item(self,contact):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return unicode(contact)

    def get_objects(self,ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return Cliente.objects.filter(pk__in=ids).order_by('nome',)