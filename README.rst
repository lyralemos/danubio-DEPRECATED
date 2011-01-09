README
======

Sobre
----------

Esse projeto foi feito exclusivamente para ser usado pela Danúbio no controle de pedidos.
É possível registrar os pedidos e seus respectivos clientes.
Tambêm é possível gerar um relatório dos pedidos de cada dia, ou de um determinado período. 

Dependencias
------------
django 1.2.x
django-admin-tools - https://bitbucket.org/izi/django-admin-tools/wiki/Home

Instalação
----------

Instalando o django::

   wget http://www.djangoproject.com/download/1.2.4/tarball/
   tar zxvf Django-1.2.4.tar.gz
   cd Django-1.2.4
   sudo python setup.py install

Instalando o django-admin-tools::

   sudo pip install django-admin-tools

ou::

   sudo easy_install django-admin-tools

Baixe o código do repositório::

   git clone https://github.com/lyralemos/danubio.git danubio
   cd danubio

Rode o syncbd::

   python manage.py syncdb