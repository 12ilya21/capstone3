"""
URL configuration for krebot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
from rebot.views import UserBookmarkCreateView, UserBookmarkDeleteView, BookmarkListView, RestaurantCoordinatesView, UserCreateView, UserListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookmark-create/', UserBookmarkCreateView.as_view()),
    path('bookmark-delete/', UserBookmarkDeleteView.as_view()),
    path('bookmark-list/', BookmarkListView.as_view()),
    path('map-coordinates/', RestaurantCoordinatesView.as_view()),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/', UserListView.as_view(), name='user-list'),
]