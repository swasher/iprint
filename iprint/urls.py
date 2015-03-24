from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('rept.urls')),
    url(r'^', include('stanzforms.urls')),

    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS

    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^login/$', 'rept.views.login', name='login'),
    url(r'^logout/$', 'rept.views.logout', name='logout'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

