from django.urls import path
from . import views

urlpatterns = [
    path('<int:book_id>/', views.book_detail, name='book_detail'),

    # Add these two wishlist paths:
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:book_id>/', views.toggle_wishlist, name='toggle_wishlist'),
]