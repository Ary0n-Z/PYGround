from django.urls import path
from hello_world import views
app_name = 'hello_world'

urlpatterns = [
    path('',views.hello_world,name='index')
]
