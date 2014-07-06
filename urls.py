from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

# from django.contrib import admin
# admin.autodiscover()

from server import urls as server_urls


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(url='app/index.html')),
    url(r'^app$', RedirectView.as_view(url='app/index.html')),

    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += server_urls.urlpatterns
