from .models import Category, Cart, Wishlist, TodaysRate
from django.utils import timezone


def store_menu(request):
    categories = Category.objects.filter(is_active=True)
    context = {
        'categories_menu': categories,
    }
    return context

def cart_menu(request):
    if request.user.is_authenticated:
        cart_items= Cart.objects.filter(user=request.user)
        context = {
            'cart_items': cart_items,
        }
    else:
        context = {}
    return context

def wishlist_count(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        count = wishlist_items.count()
    else:
        count = 0
    return {'wishlist_count': count}

def rates_context_processor(request):
    today = timezone.now().date()
    
    # Fetch gold rates for different karats
    gold_18k_rate = TodaysRate.objects.filter(metal='gold', karat=18, date=today).first()
    gold_22k_rate = TodaysRate.objects.filter(metal='gold', karat=22, date=today).first()
    gold_24k_rate = TodaysRate.objects.filter(metal='gold', karat=24, date=today).first()
    
    # Fetch silver rate
    silver_rate = TodaysRate.objects.filter(metal='silver', date=today).first()

    return {
        'gold_18k_rate': gold_18k_rate,
        'gold_22k_rate': gold_22k_rate,
        'gold_24k_rate': gold_24k_rate,
        'silver_rate': silver_rate,
    }