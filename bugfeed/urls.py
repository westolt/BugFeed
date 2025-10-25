from django.urls import path

from .views import homePageView, addView, likeView, deleteView, loginView, logoutView, signupView,infoView

urlpatterns = [
    path('', homePageView, name='index'),
    path('add/', addView, name='add'),
    path('like/<int:post_id>', likeView, name='like'),
    path('delete/<int:post_id>', deleteView, name='delete'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('signup/', signupView, name='signup'),
    path('info/', infoView, name='info')
]