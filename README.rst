README
======

Sobre
----------

Esse projeto foi feito exclusivamente para ser usado pela Dan�bio no controle de pedidos.
� poss�vel registrar os pedidos e seus respectivos clientes.
Tamb�m � poss�vel gerar um relat�rio dos pedidos de cada dia, ou de um determinado per�odo. 

Dependencias
------------
django 1.2.x
django-admin-tools - https://bitbucket.org/izi/django-admin-tools/wiki/Home

Instala��o
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

Baixe o c�digo do reposit�rio::

   git clone https://github.com/lyralemos/danubio.git danubio
   cd danubio

Rode o syncbd::

   python manage.py syncdb