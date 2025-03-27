from django.urls import path
from .views import api_home,RegisterUser, ApplyLoan
from .views import home_page

urlpatterns = [
    path('', home_page, name='home'),
    path('', api_home, name='api-home'),
    path('register-user/', RegisterUser.as_view(), name='register-user'),
    path('apply-loan/', ApplyLoan.as_view(), name='apply-loan'),
]
