from django.urls import path
from .views import *


urlpatterns = [
    path('', homepage, name='home'),
    path('delete/<int:id_link>/', delete_link, name='del'),
    path('redirect/<str:hash_url>', redirect_to_long_url, name='rdr'),
    path('register/>', RegisterUser.as_view(), name='reg'),
    path('login/', LoginUser.as_view(), name='login_user'),
    path('logout/', logout_user, name='logout'),
    path('api/', SHORTURL.as_view()),

]