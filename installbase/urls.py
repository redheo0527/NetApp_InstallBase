from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from .models import installbase

app_name = 'installbase'

urlpatterns = [
    path('', InstallBase_list.as_view(), name='installbase_list'),
    path('detail/<int:pk>', DetailView.as_view(model=installbase, template_name='installbase/detail.html'), name='installbase_detail'),
    path('upload/', InstallBase_create, name='installbase_upload'),
    path('delete/<int:pk>', InstallBase_delete.as_view(), name='installbase_delete'),
    path('update/<int:pk>', InstallBaseUpdateView, name='installbase_update'),
    path('clear/<int:pk>', InstallBaseClearView.as_view(), name='installbase_clear'),
    path('undelete/<int:pk>', InstallBase_undelete.as_view(), name='installbase_undelete'),
    path('export/', InstallBase_export, name='installbase_export'),
    path('download/<int:pk>', InstallBase_download_view, name="installbase_download"),
    path('rack_detail/<int:pk>', InstallBase_Rack_view, name='rack_detail'),
    path('rack_update/<int:pk>', InstallBase_Rack_update, name='rack_update'),
    path('storage_info/<int:pk>', storage_info, name='storage_info'),
]

