from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^inventory/$', views.inventory, name='inventory'),
    url(r'^sales/$', views.sales, name='sales'),
    url(r'^sales/add/$', views.add_sale, name='add_sale'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^register/$', views.register, name='register'),
]
