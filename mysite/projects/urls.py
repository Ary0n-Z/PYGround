from unicodedata import name
from django.urls import path
from . import views

app_name ='projects'

urlpatterns = [
    path('',views.project_index,name="index"),
    path('<int:pk>/',views.ProjectDetail.as_view(),name='detail')
]

