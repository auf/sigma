from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm

urlpatterns = patterns('',
           (r'^login/$', 'sigma.www.views.accounts.connexion'),
           (r'^logout/$', 'sigma.www.views.accounts.deconnexion'),
	   (r'^profile/$', 'sigma.www.views.general.profile'),
           (r'^password/$', 'sigma.www.views.accounts.pass_reset'),
           (r'^password_reset_confirm/(?P<uidb36>\d+)/(?P<token>[a-zA-Z0-9-]+)/$', 'sigma.www.views.accounts.pass_reset_confirm'),
           (r'^password_reset_complete/$', 'sigma.www.views.accounts.pass_reset_complete'),
           (r'^password_reset_done/$', 'sigma.www.views.accounts.pass_reset_done'),
           (r'^password_change/$', 'sigma.www.views.accounts.pass_change'),
           (r'^password_change_done/$', 'sigma.www.views.accounts.pass_change_done'),
)
