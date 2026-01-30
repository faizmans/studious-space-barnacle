from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    
    # NEW: Add this line to handle category filtering
    path('products/category/<int:category_id>/', views.product_list, name='category_filter'),
    
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),


    path('my-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('my-admin/delete/<str:model_type>/<int:pk>/', views.delete_item, name='delete_item'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),


]