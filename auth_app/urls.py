from django.urls import path
from .views import MyTokenObtainPairView

app_name = 'auth_app'

urlpatterns = [
    path('', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
