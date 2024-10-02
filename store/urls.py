from store.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, RegisterView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import gold_rates_view, GoldTypeProductListView, GoldOrnamentProductsView, category_products
from .views import  SilverTypeProductsView, SilverOrnamentView, DiamondOrnamentsView
from .views import add_to_wishlist, remove_from_wishlist, wishlist, AddressView, remove_address
from .views import submit_inquiry
from .views import order_placed


app_name = 'store'


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='store:login'), name='logout'),
    path('contact/', views.contact, name='contact'),
    path('gold-rates/', gold_rates_view, name='gold_rates'),

    path('upload_profile_image/', views.upload_profile_image, name='upload_profile_image'),

    path('search/', views.search_products, name='search_products'),
    

    # URL for Wishlist
  
    path('wishlist/add/<int:product_id>/<str:product_type>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/<str:product_type>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    
    
    # URL for Cart and Checkout
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name="remove-cart"),
    path('plus-cart/<int:cart_id>/', views.plus_cart, name="plus-cart"),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name="minus-cart"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('orders/', views.orders, name="orders"),

    #URL for Products
    path('product/<slug:slug>/', views.detail, name="product-detail"),
    path('categories/', views.all_categories, name="all-categories"),
    path('category/<slug:slug>/', views.category_products, name='category-products'),
    path('shop/', views.shop, name="shop"),
    path('gold/<str:gold_type>/', GoldTypeProductListView.as_view(), name='gold_type_products'),
    path('gold-ornaments/<str:ornament_type>/', GoldOrnamentProductsView.as_view(), name='gold_ornament_products'),
    path('silver-type/<str:silver_type>/', SilverTypeProductsView.as_view(), name='silver_type_products'),
    path('silver-ornaments/<str:silver_ornament_type>/', SilverOrnamentView.as_view(), name='silver_ornament_products'),
    path('diamonds/<str:diamond_ornament_type>/', DiamondOrnamentsView.as_view(), name='diamond_type_products'),

    #URL for Gifts
    path('gifts', views.gift_products_view, name='gifts'),
    path('gift-detail/<int:id>/', views.gift_detail, name='gift_detail'),
    
    path('accounts/profile/', views.profile, name="profile"),
    path('addresses/', AddressView.as_view(), name='address_view'),
    path('addresses/remove/<int:id>/', remove_address, name='remove_address'),

    path('accounts/password-change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html', form_class=PasswordChangeForm, success_url='/accounts/password-change-done/'), name="password-change"),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name="password-change-done"),

    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html', form_class=PasswordResetForm, success_url='/accounts/password-reset/done/'), name="password-reset"), # Passing Success URL to Override default URL, also created password_reset_email.html due to error from our app_name in URL
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name="password_reset_done"),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html', form_class=SetPasswordForm, success_url='/accounts/password-reset-complete/'), name="password_reset_confirm"), # Passing Success URL to Override default URL
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name="password_reset_complete"),

    path('product/test/', views.test, name="test"),
    
    
    # urls for customization form
    path('submit_inquiry/', views.submit_inquiry, name='submit_inquiry'),
    path('order_placed/', views.order_placed, name='order_placed'),
    path('T&C/',views.TC, name='terms'),
    path('About_us/',views.about_us, name="about_us"),
    path('help-center/',views.helpcenter, name="help-center"),
    path('FAQ/',views.FAQ, name="FAQ"),
    
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
