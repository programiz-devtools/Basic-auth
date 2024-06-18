from django.urls import path
from .views import SignUpView,LoginView,UserListView,UserDetailView

urlpatterns = [
    path("register/",SignUpView.as_view()),
    path('login/',LoginView.as_view()),
    path('users/',UserListView.as_view()),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
]