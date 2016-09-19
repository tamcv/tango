from django.conf.urls import patterns, url
from rango import views

from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
    # these are the two new imports
    password_change,
    password_change_done,
)

urlpatterns = patterns('', url(r'^$', views.index, name='index'),
                        url(r'^about/$', views.about, name='about'),
                        url(r'^add_category/$', views.add_category, name='add_category'),
                        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
                        url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
                        url(r'^accounts/password/change/$', password_change, {
                                'template_name': 'registration/password_change_form.html'},
                                name='password_change'),
                        url(r'^accounts/password/change/done/$', password_change_done,
                                {'template_name': 'registration/password_change_done.html'},
                                name='password_change_done'),
                       )