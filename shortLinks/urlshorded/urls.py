from django.urls import path
from .views import *


urlpatterns = [
    path('', homepage, name='home'),
    path('delete/<int:id_link>/', delete_link, name='del'),

]