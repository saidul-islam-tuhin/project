from django.conf.urls import url
from . import views

app_name = 'TutionFee'

urlpatterns = [
    url(r'^Home/$', views.home, name='home'),
    url(r'^Home/(?P<subject>\w+)$', views.subject_wise, name='subject_wise'),
]
