from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jaksafe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(url=reverse_lazy('report_auto')), name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^report/', include('report.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
)

# serve static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
