from django.db.models import Q

from ajax_select import LookupChannel

from pedidos.models import Cliente

class ClienteLookup(LookupChannel):

    model = Cliente

    def get_query(self,q,request):
        return Cliente.objects.filter(Q(nome__icontains=q)).order_by('nome')

    def get_result(self,obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.nome

    def format_match(self,obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"<b>%s</b> <br />%s" % (obj.nome,obj.telefone1)
