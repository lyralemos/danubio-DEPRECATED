$(document).ready(function(){

	//ajusta a navegacao
	loc = String(location)
	if(loc.search('produtos') != -1){
		$('#produtos-nav').addClass('active')
	}else if(loc.search('clientes') != -1){
		$('#clientes-nav').addClass('active')
	}else if(loc.search('pedidos') != -1){
		$('#pedidos-nav').addClass('active')
	}else{
		$('#index-nav').addClass('active')
	}


	$('#add').click(function(){
		titulo = $(this).html()
		$.get('add',function(data){
			$('#main-modal').html(data).modal()
			make_ajax_form('add',0)
			$('.modal-header h3').html(titulo)
		})
		return false
	})

	$('#object_list a').click(function(){
		id = $(this).attr('data-id')
		if (id){	
			titulo = $(this).attr('data-titulo')
			$.get('update/'+id,function(data){
				$('#main-modal').html(data).modal()
				make_ajax_form('update',id)
				$('.modal-header h3').html(titulo)
			})
			return false
		}
	})

	$('#id_cliente_on_deck').bind('added',function(){
		id_cliente = $('#id_cliente').val()
		get_enderecos(id_cliente,null)
	})

	$('#itens-pedido td:first-child').each(function(){
		var td = $(this)
		var elm = td.find('select')
		if (elm.val()){
			get_valor_unitario(td,elm.val())
		}
	})

	$('.quantidade').each(function(){
		var elm = $(this)
		var input = elm.find('input')

		input
			.bind('keyup click blur focus change paste',function(){
				quantidade = parseFloat($(this).val())
				get_sub_total(elm)
			})
			.next().click(function(){
				input = $(this).prev()
				if (input.val() && input.val()>=0){
					input.val(parseInt(input.val())+1)
					input.focus()
				}
			})
			.next().click(function(){
				input = $(this).prev().prev()
				if (input.val() && input.val()>0){
					input.val(parseInt(input.val())-1)
					input.focus()
				}
			})
	})

	$('#id_data_entrega').datepicker({
		format : 'dd/mm/yyyy',
		language: 'pt-BR'
	})
	$('#id_observacao').addClass('input-xxlarge')

	if (!$('#id_endereco option:selected').val()){
		$('#id_endereco option').remove()
	}else if ($('#id_cliente').val()){
		get_enderecos($('#id_cliente').val())
	}

	//fix para links com paramertos get
	$('a[data-href]').attr('href', function(index, href) {
        var param = $(this).data('href')
        key = param.split('=')[0]
        value = param.split('=')[1]

        href = document.location.href
        params = getParameters()
        result = '?'

        for (p in params)
        	if (key != p)
        		result += p + '=' + params[p] + '&'
        result += key + '=' + value

        return result

    });

    $('#q-field').focus(function(e){
    	$(this).animate({width:'250px'},100)
    }).blur(function(e){
    	$(this).animate({width:'150px'},100)
    })

    $('select#id_cliente').chosen({
    	no_results_text: "Nenhum resultado encontrado"
    }).change(function(e){
    	get_enderecos($(this).val(),null)
    })

    $('td.produto select').chosen({
    	no_results_text: "Nenhum resultado encontrado"
    }).change(function(){
    	get_valor_unitario($(this).parent(),$(this).val())
    })
	
})

get_valor_unitario = function(elm,id){
	$.getJSON('/pedidos/get_price/'+id,function(data){
		elm.next().find('input').val(data.price)
		get_sub_total(elm.next().next())
		atualiza_total()
	})
}

get_sub_total = function(elm){
	quantidade = parseFloat(elm.find('input').val())
	unidade = parseFloat(elm.prev().find('input').val())
	elm.next().find('input').val(unidade*quantidade)
	atualiza_total()
}

get_enderecos = function(id,selected){
	$('#id_endereco option').remove()
	$.getJSON('/pedidos/get_endereco/'+id,function(data){
		for(i=0;i<data.length;i++){
			endereco = data[i]
			if (selected && endereco.pk == id)
				$('#id_endereco').append('<option value="'+endereco.pk+'" selected="selected">'+endereco.nome+'</option>')
			else
				$('#id_endereco').append('<option value="'+endereco.pk+'">'+endereco.nome+'</option>')
		}
		$('#field-endereco').show('fast')
	})
}

atualiza_total = function(){
	var valor = 0.0
	var desconto = parseFloat($('#desconto').html())
	$('.sub_total input').each(function(){
		valor += parseFloat($(this).val())
	})
	total = valor-desconto
	$('#valor').html(String(valor.toFixed(2)).replace('.',','))
	$('#total').html(String(total.toFixed(2)).replace('.',','))
}

make_ajax_form = function(action,id){
	if(action == 'add'){
		$('#delete').hide()
		href = action+'/'
		$('#frm').attr('action',href)
	}else{
		$('#delete').attr('href','delete/'+id)
		href = action+'/'+id+'/'
		$('#frm').attr('action',href)
	}
	$('#frm').submit(function(){
		$.post(href,$('#frm').serialize(),function(data){
			if (data.indexOf('errorlist') !== -1){
				$('#main-modal').html(data)
				make_ajax_form(action,id)
			}else{
				location.reload()
			}
		})
		return false
	})
		
}

function getParameters() {
	var searchString = window.location.search.substring(1)
	var params = searchString.split("&")
	var hash = {}

	if (searchString == ""){
		return null
	}

	for (var i = 0; i < params.length; i++) {
		var val = params[i].split("=");
		hash[unescape(val[0])] = unescape(val[1]);
	}
	return hash;
}