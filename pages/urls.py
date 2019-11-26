from django.conf.urls import url,include
from .views import home, page

urlpatterns = [
    url(r'^$', home),
    url(r'^(?P<slug>[-\w]+)/$', page),
]