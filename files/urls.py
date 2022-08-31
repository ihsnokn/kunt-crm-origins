

from django.urls import path


from . import views
app_name = "files"

urlpatterns = [
  path('file-delete-update/', views.FileDeleteUpdate, name='file-delete-update'),
  #  path('', FileListView.as_view(), name='file-list'),
    path('', views.FileListView, name='file-list'),
   # path('<int:pk>/', FileDetailView.as_view(), name='file-detail'),
    path('<int:pk>/', views.FileDetail, name='filedetail'),
    # path('<int:pk>/update', FileUpdateView.as_view(), name='file-update'),
    path('<int:pk>/update', views.FileUpdateView, name='file-update'),
    path('<int:pk>/update/fee', views.FileUpdateFeeView, name='file-update-fee'),
   # path('<int:pk>/delete', FileDeleteView.as_view(), name='file-delete'),
    path('<int:pk>/delete/', views.file_delete, name='file-delete'),

    
    
    path('create/', views.FileCreateView, name='File_create'),
    path('sign_out/', views.sign_out, name='sign_out'),
    #path('create/', FileCreateView.as_view(), name='file-create'),
]
