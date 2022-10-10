from django.urls import path
from .views import *


urlpatterns = [
    path('', homepage, name='home'),
    path('delete/<int:id_link>/', delete_link, name='del'),
    path('redirect/<str:hash_url>', redirect_to_long_url, name='rdr'),
    path('register/>', RegisterUser.as_view(), name='reg'),
    path('login/', login_users, name='log_user'),

]