"""
URL configuration for gifts_rec project.

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
from django.conf.urls.static import static
from app import views
from .settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello, name="home"),
    path('products-list', views.products_list, name="products-list"),
    path('product/<int:id>/', views.product, name="product-page"),
    path('toggle-favourite/<int:id>/', views.toggle_favourite, name='toggle-favourite'),
    path('favourites', views.favourite_list, name="favourite-list"),
    path('favourites/<int:user_id>/', views.favourite_list, name='favourite-list-user'),
    path('register', views.custom_register, name="register"),
    path('login', views.custom_login, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('questionnaire', views.questionnaire, name='questionnaire'),
    path('questionnaire/<str:user_id>', views.questionnaire_res, name='questionnaire_res'),
    path('delete-friend/<int:friend_id>/', views.delete_friend, name='delete-friend'),
    path('friends/', views.friends_page, name='friends-page'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
