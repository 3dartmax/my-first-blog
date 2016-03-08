from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
	#url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
	url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
	url(r'^post/new/$', views.post_new, name='post_new'),
	#url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),	
	url(r'^post/test1_1/$', views.post_test1_1),
	url(r'^post/test1_2/$', views.post_test1_2),
	url(r'^post/test1_3/$', views.post_test1_3),
	url(r'^post/test1_4/$', views.post_test1_4),
]
