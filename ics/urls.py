from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from .models import ics_part,ics_inout

app_name = 'ics'

urlpatterns = [
    path('', part_list.as_view(), name='part_list'),
    path('upload/', part_create, name='part_upload'),
    path('inout/<int:pk>', inout_create, name='part_inout'),
    path('inout_del/<int:pk>,<int:inoutid>', inout_delete, name='part_inout_delete'),
]
