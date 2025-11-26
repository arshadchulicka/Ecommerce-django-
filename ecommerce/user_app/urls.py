from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register/", views.Register_user, name="Register_user"),
    path("login/", views.session_login, name="session_login"),
    path("logout/", views.session_logout, name="session_logout"),

    path("dashboard/", views.session_dashboard, name="session_dashboard"),

    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:cart_id>/', views.remove_cart, name='remove_cart'),

    path('checkout/', views.checkout, name='checkout'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)