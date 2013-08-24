from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from ajax_select import urls as ajax_select_urls

urlpatterns = patterns('',
    # Login / logout.
    url(r'^login/$', 'django.contrib.auth.views.login',name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',name="logout"),
    (r'^lookups/', include(ajax_select_urls)),
    (r'^admin/', include(admin.site.urls)),
    (r'',include('pedidos.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )