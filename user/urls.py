from django.conf.urls import url
from . import views as userview

urlpatterns = [
    url(r'^dashboard$', userview.dashboard, name='dashboard'),
    url(r'^dashboard/profile/$', userview.profile, name='profile'),
    url(r'^dashboard/upload/$', userview.upload, name='upload'),
    url(r'^dashboard/download/$', userview.download, name='download'),
    url(r'^dashboard/history/$', userview.history, name='history'),
    url(r'^dashboard/history/clear$', userview.clear_history, name='clear_history'),
    url(r'^dashboard/chngpass/$', userview.chngpass, name='chngpass'),
    url(r'^dashboard/sendmail/$', userview.sendmail, name='sendmail')
]
