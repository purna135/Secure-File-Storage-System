from django.conf.urls import url
from . import views as home_view

urlpatterns=[
    url(r'^$', home_view.indexview, name='indexview'),

    url(r'^changepass$', home_view.changepass, name = 'changepass'),
    url(r'^saveimg$', home_view.save_image, name = 'changepass_save_img'),
    url(r'^updatepass/$', home_view.updatepass, name = 'updatepass'),

    url(r'^signin/$', home_view.signinview, name='signinview'),
    url(r'^signin/saveimg', home_view.save_image, name='signin_save_img'),

    url(r'^signup/$', home_view.signupview, name='signupview'),
    url(r'^signup/saveimg', home_view.save_image, name='signup_save_img'),

    url(r'^logout/$', home_view.logoutview, name='logoutview')
]
