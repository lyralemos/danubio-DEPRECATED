from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from ajax_select import urls as ajax_select_urls

urlpatterns = patterns('',
    # Example:
    # (r'^danubio/', include('danubio.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^lookups/', include(ajax_select_urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'',include('danubio.pedidos.urls')),
    # Login / logout.
    url(r'^login/$', 'django.contrib.auth.views.login',name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',name="logout"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )