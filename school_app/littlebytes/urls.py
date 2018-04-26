from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^help/$', views.help, name='help'),
    url(r'^inventory/$', views.inventory, name='inventory'),
    url(r'^inventory/update/$', views.inventory_update, name='inventory_update'),
    url(r'^sales/$', views.sales, name='sales'),
    url(r'^sales/add/$', views.add_sale, name='add_sale'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^register/$', views.register, name='register'),
]
