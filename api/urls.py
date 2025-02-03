from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("books/", views.BookListCreateView.as_view(), name="books-list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("users/", views.UserListCreateView.as_view(), name="users-list"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.CustomTokenObtainPairView.as_view(), name="login"),
    path(
        "checkout/<int:book_id>/",
        views.CheckoutBookView.as_view(),
        name="checkout-book",
    ),
    path(
        "return/<int:transaction_id>/",
        views.ReturnBookView.as_view(),
        name="return-book",
    ),
    path(
        "transactions/", views.TransactionsListView.as_view(), name="transactions-list"
    ),
    path(
        "profile/",
        views.ProfileView.as_view(),
        name="profile",
    ),
]
