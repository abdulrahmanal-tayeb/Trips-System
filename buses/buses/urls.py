"""
URL configuration for buses project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ="token_obtain_pair"),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path('signin/', SignInAPIView.as_view()),
    path('signup/', SignUpAPIView.as_view()),
    path('admin/', admin.site.urls),
    path('api/v1/buses/', BusAPIView.as_view()),
    path('api/v1/tickets/', TicketAPIView.as_view()),
    path('api/v1/user/tickets/', TicketHistoryAPIView.as_view()),
    path('api/v1/trips/', TripAPIView.as_view()),
    path('api/v1/destinations/create/', DestinationAPIView.as_view()),
    path('api/v1/trips/search/', trip_search)
]
