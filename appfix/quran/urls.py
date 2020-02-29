from django.conf.urls import url
from . import views

app_name = 'quran'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<qori_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<murotal_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^murotals/(?P<filter_by>[a-zA_Z]+)/$', views.murotals, name='murotals'), 
    url(r'^create_qori/$', views.create_qori, name='create_qori'),
    url(r'^(?P<qori_id>[0-9]+)/create_murotal/$', views.create_murotal, name='create_murotal'),
    url(r'^(?P<qori_id>[0-9]+)/delete_murotal/(?P<murotal_id>[0-9]+)/$', views.delete_murotal, name='delete_murotal'),
    url(r'^(?P<qori_id>[0-9]+)/favorite_qori/$', views.favorite_qori, name='favorite_qori'),
    url(r'^(?P<qori_id>[0-9]+)/delete_qori/$', views.delete_qori, name='delete_qori'),
]
