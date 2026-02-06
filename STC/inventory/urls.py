from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    
    path('products/category/<int:category_id>/', views.product_list, name='category_filter'),
    
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),


    path('my-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('my-admin/delete/<str:model_type>/<int:pk>/', views.delete_item, name='delete_item'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('quote/add/<int:product_id>/', views.add_to_quote, name='add_to_quote'),
    path('quote/remove/<int:product_id>/', views.remove_from_quote, name='remove_from_quote'),
    path('quote/basket/', views.quote_list, name='quote_list'),

    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

    path('subscribe/', views.subscribe, name='subscribe'),

]