from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import index, index_ja, health, input_test

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', input_test, name='input_test'),
    url(r'^en$', index),
    url(r'^ja$', index_ja),
    url(r'^health$', health),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
