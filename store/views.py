import django
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from store.models import Address, Cart, Category, Order,  Wishlist, TodaysRate, CarousalImage, Specials
from django.utils import timezone
from store.models import ContactSubmission
from django.shortcuts import redirect, render, get_object_or_404

from store.utils import send_registration_message

# from store.utils import fetch_phone_numbers, send_whatsapp_message
from .forms import AddressForm, SortForm
from django.contrib import messages
from django.views import View
from decimal import Decimal
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import GoldProduct, SilverProduct, DiamondProduct, Category,TodaysRate, ProductImage, GiftProduct, CustomizationInquiry, Profile
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomizationInquiryForm
from .forms import SortForm, SearchForm
from django.db.models import Q

class CustomLoginView(LoginView):
    template_name = 'registration/registration.html'  # This is the template where both forms (login and register) reside
    form_class = AuthenticationForm  # Use the built-in authentication form

    # To redirect to a specific page after login
    def get_success_url(self):
        return reverse_lazy('store:home')  # Change this to the page you want after login


# Custom Register View

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/registration.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number = request.POST.get('phone_number')  # Get phone number from form

        # Validation and user creation
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            else:
                # Create user
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                # Check if profile exists before creating a new one
                profile, created = Profile.objects.get_or_create(user=user)
                profile.phone_number = phone_number  # Save the phone number
                profile.save()

                # Send WhatsApp welcome message after successful registration
                apikey = "e45c575504914d1e982df8674958864a"
                send_registration_message(apikey, phone_number, username)

                messages.success(request, "Your account has been successfully created!")
                return redirect('store:login')
        else:
            messages.error(request, "Passwords do not match")

        return render(request, 'registration/registration.html')


    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('store:home')


@login_required
def profile(request):
    user = request.user
    addresses = Address.objects.filter(user=user)
    orders = Order.objects.filter(user=user)
    context = {
        'addresses': addresses,
        'orders': orders,
    }
    return render(request, 'account/profile.html', context)




@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            profile = Profile.objects.get(user=request.user)
            profile.profile_image = profile_image
            profile.save()
            messages.success(request, 'Profile image updated successfully!')
        else:
            messages.error(request, 'Please select a valid image file.')
    return redirect('store:profile')  # Adjust this URL to match your profile page


def search_products(request):
    form = SearchForm(request.GET or None)
    query = request.GET.get('query', '').strip().lower()

    # Create a Q object to handle more complex queries
    search_query = Q(title__icontains=query)
    
    # Filter products using the search query
    gold_products = GoldProduct.objects.filter(search_query)
    silver_products = SilverProduct.objects.filter(search_query)
    diamond_products = DiamondProduct.objects.filter(search_query)
    
    context = {
        'form': form,
        'gold_products': gold_products,
        'silver_products': silver_products,
        'diamond_products': diamond_products,
    }
    return render(request, 'store/search_results.html', context)



def home(request):

    # apikey = "e45c575504914d1e982df8674958864a"
    # mobile_numbers_list = fetch_phone_numbers()  # List of numbers
    # message = "testing through code"

    # # Call the function for a list of numbers
    # result_list = send_whatsapp_message(apikey, mobile_numbers_list, message)
    # print(result_list)
    # Fetching categories and featured products
    categories = Category.objects.filter(is_active=True, is_featured=True)[:3]

    # Fetching gold, silver, and diamond products
    gold_products = GoldProduct.objects.filter(is_active=True, is_featured=True)[:4]
    silver_products = SilverProduct.objects.filter(is_active=True, is_featured=True)[:4]
    diamond_products = DiamondProduct.objects.filter(is_active=True, is_featured=True)[:4]

    # Adding total amount and discounted price to each product
    for product in gold_products:
        product.total_amount = product.calculate_total_amount()
        product.discounted_price = product.get_discounted_price
        product.type = 'gold'

    for product in silver_products:
        product.total_amount = product.calculate_total_amount()
        product.discounted_price = product.get_discounted_price
        product.type = 'silver'

    for product in diamond_products:
        product.total_amount = product.calculate_total_amount()
        product.discounted_price = product.get_discounted_price
        product.type = 'diamond'

    # Fetching carousal images and special images
    carousal_images = CarousalImage.objects.all()
    special_images = Specials.objects.all()

    # Fetching today's gold and silver rates
    today = timezone.now().date()
    gold_rate = TodaysRate.objects.filter(metal='gold', date=today).first()
    silver_rate = TodaysRate.objects.filter(metal='silver', date=today).first()

    context = {
        'categories': categories,
        'gold_products': gold_products,
        'silver_products': silver_products,
        'diamond_products': diamond_products,
        'carousal_images': carousal_images,
        'special_images': special_images,
        'gold_rate': gold_rate,
        'silver_rate': silver_rate,
    }

    return render(request, 'store/index.html', context)



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactSubmission.objects.create(name=name, email=email, message=message)
        messages.success(request, 'Thank you for your message.')
        return redirect('store:contact')

    return render(request, 'store/contact.html')


def gift_products_view(request):
    gifts = GiftProduct.objects.all()  # Retrieve all GiftProduct instances
    return render(request, 'store/gifts.html', {'gifts': gifts})


def gift_detail(request, id):
    gift_product = get_object_or_404(GiftProduct, id=id)
    category_slug = gift_product.category.slug

    context = {
        'gift_product': gift_product,
        'category_url': reverse('category-products', args=[category_slug])
        }
    
    return render(request, 'store/gift_detail.html', context)


    


class GoldTypeProductListView(ListView):
    template_name = 'store/gold_type_products.html'
    context_object_name = 'products'
    
    if GoldProduct.fixed_mrp_price:
        price = GoldProduct.fixed_mrp_price
    else:
        
         price = GoldProduct.gold_rate + GoldProduct.making_charge + GoldProduct.gst

    def get_queryset(self):
        gold_type = self.kwargs['gold_type']  # Assuming URL captures gold type
        queryset = GoldProduct.objects.filter(gold=gold_type, is_active=True, is_featured=True)
       
            
        
        # Calculate total amount for each product
        for product in queryset:
            product.total_amount = product.calculate_total_amount()
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gold_type'] = self.kwargs['gold_type']
        return context


class GoldOrnamentProductsView(ListView):
    template_name = 'store/gold_ornament_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        ornament_type = self.kwargs['ornament_type']  # Assuming URL captures ornament type
        queryset = GoldProduct.objects.filter(gold_ornament_type=ornament_type, is_active=True, is_featured=True)
        
        # Calculate total amount for each product
        for product in queryset:
            product.total_amount = product.calculate_total_amount()
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['metal'] = 'gold'
        context['ornament_type'] = self.kwargs['ornament_type']
        return context




class SilverTypeProductsView(ListView):
    template_name = 'store/silver_type_products.html'
    context_object_name = 'products'
    
    # Calculate prices
    if SilverProduct.fixed_mrp_price:
        price = SilverProduct.fixed_mrp_price
    else:
        
         price = SilverProduct.silverrate + SilverProduct.making_charge + SilverProduct.gst
    
 
    def get_queryset(self):
        silver_type = self.kwargs['silver_type']
        return SilverProduct.objects.filter(silver_type=silver_type, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['silver_type'] = self.kwargs['silver_type']
        return context
    

    

class SilverOrnamentView(ListView):
    template_name = 'store/silver_ornament_products.html'
    context_object_name = 'products'
   
    
       


    def get_queryset(self):
        silver_ornament_type = self.kwargs['silver_ornament_type']
        return SilverProduct.objects.filter(silver_ornament_type=silver_ornament_type, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['silver_ornament_type'] = self.kwargs['silver_ornament_type']
        return context





class DiamondOrnamentsView(ListView):
    model = DiamondProduct
    template_name = 'store/diamond_ornament_list.html'
    context_object_name = 'products'
    
    if DiamondProduct.fixed_mrp_price:
        price = DiamondProduct.fixed_mrp_price
    else:
        
        price = DiamondProduct.gold_rate +DiamondProduct.making_charge + DiamondProduct.gst

    def get_queryset(self):
        diamond_ornament_type = self.kwargs['diamond_ornament_type']
        return DiamondProduct.objects.filter(diamond_ornament_type=diamond_ornament_type, is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diamond_ornament_type'] = self.kwargs['diamond_ornament_type']
        return context



from django.shortcuts import get_object_or_404, redirect, render
from .models import GoldProduct, SilverProduct, DiamondProduct, ProductImage
from .forms import SortForm

def detail(request, slug):
    product = None
    product_type = None
    form = None

    if GoldProduct.objects.filter(slug=slug).exists():
        product = get_object_or_404(GoldProduct, slug=slug)
        product_type = 'gold'
    elif SilverProduct.objects.filter(slug=slug).exists():
        product = get_object_or_404(SilverProduct, slug=slug)
        product_type = 'silver'
    elif DiamondProduct.objects.filter(slug=slug).exists():
        product = get_object_or_404(DiamondProduct, slug=slug)
        product_type = 'diamond'

    if product is None:
        return redirect('some_error_page')  # or handle the error appropriately

    if request.method == 'POST':
        form = SortForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_detail', slug=product.slug)
    else:
        form = SortForm()

    images = ProductImage.objects.filter(
        gold_product=product if product_type == 'gold' else None,
        silver_product=product if product_type == 'silver' else None,
        diamond_product=product if product_type == 'diamond' else None
    )

    related_products = []
    if product_type == 'gold':
        related_products = GoldProduct.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    elif product_type == 'silver':
        related_products = SilverProduct.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    elif product_type == 'diamond':
        related_products = DiamondProduct.objects.exclude(id=product.id).filter(is_active=True, category=product.category)

    # Calculate prices
    price = None
    making_charges = product.making_charges
    gst_amount = product.gst_amount

    if product.fixed_mrp_price:
        price = product.fixed_mrp_price
    else:
        if product_type == 'gold':
            if product.gold_rate and product.gold_rate.rate is not None:
                price = product.gold_rate.rate + making_charges + gst_amount
            else:
                # Handle case where gold_rate is None
                price = making_charges + gst_amount
        elif product_type == 'silver':
            if product.gold_rate and product.gold_rate.rate is not None:
                price = product.gold_rate.rate + making_charges + gst_amount
            else:
                # Handle case where gold_rate is None
                price = making_charges + gst_amount
        elif product_type == 'diamond':
            price = product.diamond_price + making_charges + gst_amount

    total_amount = product.calculate_total_amount()
    karatage = getattr(product, 'karatage', None)
    discounted_price = product.get_discounted_price()

    context = {
        'product': product,
        'product_type': product_type,
        'related_products': related_products,
        'images': images,
        'making_charges': making_charges,
        'gst_amount': gst_amount,
        'total_amount': total_amount,
        'karatage': karatage,
        'discounted_price': discounted_price,
        'form': form,
        'price': price,
    }
    return render(request, 'store/detail.html', context)




def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'store/categories.html', {'categories':categories})




def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    gold_products = GoldProduct.objects.filter(is_active=True, category=category)
    silver_products = SilverProduct.objects.filter(is_active=True, category=category)
    diamond_products = DiamondProduct.objects.filter(is_active=True, category=category)
    
    # Handle price filtering
    sort_option = request.GET.get('sort')
    if sort_option == 'low_to_high':
        gold_products = gold_products.order_by('price')
        silver_products = silver_products.order_by('price')
        diamond_products = diamond_products.order_by('price')
    elif sort_option == 'high_to_low':
        gold_products = gold_products.order_by('-price')
        silver_products = silver_products.order_by('-price')
        diamond_products = diamond_products.order_by('-price')

    # Handle karatage filtering
    karatage_values = request.GET.getlist('karatage')
    if karatage_values:
        gold_products = gold_products.filter(karatage__in=karatage_values)
        silver_products = silver_products.filter(karatage__in=karatage_values)
        diamond_products = diamond_products.filter(karatage__in=karatage_values)

    categories = Category.objects.filter(is_active=True)
    context = {
        'category': category,
        'gold_products': gold_products,
        'silver_products': silver_products,
        'diamond_products': diamond_products,
        'categories': categories,
    }
    return render(request, 'store/category_products.html', context)





@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'account/add_address.html', {'form': form, 'addresses': addresses})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            pin_code = form.cleaned_data['pin_code']
            state = form.cleaned_data['state']
            Address.objects.create(user=request.user, locality=locality, city=city, pin_code=pin_code, state=state)
            messages.success(request, "New Address Added Successfully.")
            return redirect('store:profile')
        else:
            messages.error(request, "Failed to add new address. Please correct the errors below.")
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'account/add_address.html', {'form': form, 'addresses': addresses})



@login_required
def remove_address(request, id):
    address = get_object_or_404(Address, user=request.user, id=id)
    if request.method == 'POST':
        address.delete()
        messages.success(request, "Address removed successfully.")
    else:
        messages.error(request, "Failed to remove address. Please use POST method.")

    return redirect('store:profile')




def wishlist_view(request):
    # Your view logic here
    return render(request, 'wishlist.html')


@login_required
def add_to_cart(request):
    user = request.user
    product_slug = request.GET.get('prod_slug')
    product_type = None  # Variable to store the product type

    # Determine the product type based on its existence in each type of product
    if GoldProduct.objects.filter(slug=product_slug).exists():
        product = get_object_or_404(GoldProduct, slug=product_slug)
        product_type = 'gold'
    elif SilverProduct.objects.filter(slug=product_slug).exists():
        product = get_object_or_404(SilverProduct, slug=product_slug)
        product_type = 'silver'
    elif DiamondProduct.objects.filter(slug=product_slug).exists():
        product = get_object_or_404(DiamondProduct, slug=product_slug)
        product_type = 'diamond'
    else:
        messages.error(request, "Product does not exist.")
        return redirect('store:home')

    # Check whether the Product is already in Cart or Not
    if product_type == 'gold':
        item_already_in_cart = Cart.objects.filter(user=user, gold_product=product).exists()
        if item_already_in_cart:
            cart_item = Cart.objects.get(user=user, gold_product=product)
    elif product_type == 'silver':
        item_already_in_cart = Cart.objects.filter(user=user, silver_product=product).exists()
        if item_already_in_cart:
            cart_item = Cart.objects.get(user=user, silver_product=product)
    elif product_type == 'diamond':
        item_already_in_cart = Cart.objects.filter(user=user, diamond_product=product).exists()
        if item_already_in_cart:
            cart_item = Cart.objects.get(user=user, diamond_product=product)
    else:
        item_already_in_cart = False

    if item_already_in_cart:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"{product.title} quantity updated in your cart.")
    else:
        if product_type == 'gold':
            Cart.objects.create(user=user, gold_product=product)
        elif product_type == 'silver':
            Cart.objects.create(user=user, silver_product=product)
        elif product_type == 'diamond':
            Cart.objects.create(user=user, diamond_product=product)
        messages.success(request, f"{product.title} added to your cart.")

    return redirect('store:cart')



def gold_rates_view(request):
    # Fetch gold rates for all karats
    gold_rates = {}
    karat_choices = [18, 22, 24]
    
    for karat in karat_choices:
        latest_rate = TodaysRate.objects.filter(metal='gold', karat=karat).order_by('-date').first()
        gold_rates[karat] = latest_rate

    # Fetch the latest silver rate
    silver_rate = TodaysRate.objects.filter(metal='silver').order_by('-date').first()

    context = {
        'gold_rates': gold_rates,
        'silver_rate': silver_rate,
    }

    return render(request, 'store/index.html', context)



@login_required
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user).first()
    if not wishlist:
        wishlist = Wishlist(user=request.user)
        wishlist.save()
    context = {
        'wishlist': wishlist
    }
    return render(request, 'store/wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id, product_type):
    product = None
    if product_type == 'gold':
        product = get_object_or_404(GoldProduct, id=product_id)
    elif product_type == 'silver':
        product = get_object_or_404(SilverProduct, id=product_id)
    elif product_type == 'diamond':
        product = get_object_or_404(DiamondProduct, id=product_id)
    
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product_type == 'gold':
        wishlist.gold_products.add(product)
    elif product_type == 'silver':
        wishlist.silver_products.add(product)
    elif product_type == 'diamond':
        wishlist.diamond_products.add(product)
    
    return redirect('store:wishlist')

@login_required
def remove_from_wishlist(request, product_id, product_type):
    product = None
    if product_type == 'gold':
        product = get_object_or_404(GoldProduct, id=product_id)
    elif product_type == 'silver':
        product = get_object_or_404(SilverProduct, id=product_id)
    elif product_type == 'diamond':
        product = get_object_or_404(DiamondProduct, id=product_id)
    
    wishlist = Wishlist.objects.filter(user=request.user).first()
    
    if product_type == 'gold':
        wishlist.gold_products.remove(product)
    elif product_type == 'silver':
        wishlist.silver_products.remove(product)
    elif product_type == 'diamond':
        wishlist.diamond_products.remove(product)
    
    return redirect('store:wishlist')


@login_required
def cart(request):
    user = request.user
    
    # Fetch cart products for the current user
    cart_products = Cart.objects.filter(user=user)

    try:
        # Fetch today's gold rate
        today_gold_rate = TodaysRate.objects.filter(metal='gold').latest('date').rate
    except TodaysRate.DoesNotExist:
        today_gold_rate = None  # Handle this case as per your application's requirements

    # Update prices of products in the cart based on today's gold rate
    if today_gold_rate is not None:
        for cart_item in cart_products:
            if cart_item.gold_product:
                cart_item.gold_product.update_price_based_on_gold_rate(today_gold_rate)
                cart_item.gold_product.save()

    # Refresh cart_products to reflect updated prices
    cart_products = Cart.objects.filter(user=user)

    # Calculate total price
    total_price = sum(cart_item.total_price for cart_item in cart_products)

    # Fetch customer addresses
    addresses = Address.objects.filter(user=user)

    # Fetch wishlist items count
    wishlist_count = Wishlist.objects.filter(user=user).count()

    # Prepare context data
    context = {
        'cart_products': cart_products,
        'total_price': total_price,
        'grand_total': total_price,
        'addresses': addresses,
        'today_gold_rate': today_gold_rate,  # Pass the gold rate to the template if needed
        'wishlist_count': wishlist_count,  # Add wishlist count to the context
    }
    
    # Render the cart template with context data
    return render(request, 'store/cart.html', context)



@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        cart_item = get_object_or_404(Cart, id=cart_id)
        cart_item.delete()
        # messages.success(request, "Product removed from Cart.")
    return redirect('store:cart')




@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cart_item = get_object_or_404(Cart, id=cart_id)
        cart_item.quantity += 1
        cart_item.save()
    return redirect('store:cart')




@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cart_item = get_object_or_404(Cart, id=cart_id)
        
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
    
    return redirect('store:cart')



@login_required
def checkout(request):
    user = request.user
    address_id = request.GET.get('address')
    
    if address_id is not None:
        # Retrieve the address selected by the user
        address = get_object_or_404(Address, id=address_id, user=user)
        
        # Fetch cart items for the current user
        cart_items = Cart.objects.filter(user=user)
        
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty. Cannot proceed with checkout.')
            return redirect('store:cart')

        try:
            # Fetch today's gold rate
            today_gold_rate = TodaysRate.objects.filter(metal='gold').latest('date').rate
        except TodaysRate.DoesNotExist:
            messages.error(request, 'Gold rate for today is not available. Cannot proceed with checkout.')
            return redirect('store:cart')
        
        total_amount = decimal.Decimal(0)
        for cart_item in cart_items:
            if cart_item.gold_product:
                product = cart_item.gold_product
                # Update the corresponding CustomizationInquiry
                CustomizationInquiry.objects.filter(product_name=product.title).update(has_placed_order=True)
            elif cart_item.silver_product:
                product = cart_item.silver_product
                # Update the corresponding CustomizationInquiry
                CustomizationInquiry.objects.filter(product_name=product.title).update(has_placed_order=True)
            elif cart_item.diamond_product:
                product = cart_item.diamond_product
                # Update the corresponding CustomizationInquiry
                CustomizationInquiry.objects.filter(product_name=product.title).update(has_placed_order=True)
            else:
                messages.error(request, 'Product not found in the cart.')
                return redirect('store:cart')
            
            product_amount = product.weight * today_gold_rate
            total_amount += product_amount * cart_item.quantity
            
            Order.objects.create(
                user=user,
                address=address,
                gold_product=cart_item.gold_product,
                silver_product=cart_item.silver_product,
                diamond_product=cart_item.diamond_product,
                quantity=cart_item.quantity,
                total_amount=product_amount * cart_item.quantity  # Assuming this is a field in your Order model
            )
            
            cart_item.delete()
        
        messages.success(request, 'Order placed successfully!')
        return redirect('store:orders')
    
    else:
        messages.error(request, 'Please select an address before proceeding or add your address in your profile section.')
        return redirect('store:cart')


@login_required
def orders(request):
    # Fetch all orders placed by the current user, ordered by ordered_date descending
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    
    # Render the orders.html template with the fetched orders
    return render(request, 'store/orders.html', {'orders': all_orders})


def shop(request):
    return render(request, 'store/shop.html')

def test(request):
    return render(request, 'store/test.html')


def create_or_update_product(request, product_data):
    # Extract common data for creating or updating product
    title = product_data.get('title')
    slug = product_data.get('slug')
    sku = product_data.get('sku')
    short_description = product_data.get('short_description')
    detail_description = product_data.get('detail_description')
    weight = product_data.get('weight')
    category_id = product_data.get('category')
    is_active = product_data.get('is_active')
    is_featured = product_data.get('is_featured')

    # Fetch today's gold rate
    today_gold_rate = TodaysRate.objects.latest('date').rate

    # Calculate the price based on the weight and today's gold rate
    price = weight * today_gold_rate

    # Check if the product already exists
    product_id = product_data.get('id')
    if product_id:
        # Update existing product
        if product_data.get('gold_product'):
            product = GoldProduct.objects.get(id=product_id)
        elif product_data.get('silver_product'):
            product = SilverProduct.objects.get(id=product_id)
        elif product_data.get('diamond_product'):
            product = DiamondProduct.objects.get(id=product_id)

        product.title = title
        product.slug = slug
        product.sku = sku
        product.short_description = short_description
        product.detail_description = detail_description
        product.weight = weight
        product.category_id = category_id
        product.is_active = is_active
        product.is_featured = is_featured
        product.save()

    else:
        # Create new product
        if product_data.get('gold_product'):
            product = GoldProduct.objects.create(
                title=title,
                slug=slug,
                sku=sku,
                short_description=short_description,
                detail_description=detail_description,
                weight=weight,
                category_id=category_id,
                is_active=is_active,
                is_featured=is_featured,
                price=price  # Set price
            )
        elif product_data.get('silver_product'):
            product = SilverProduct.objects.create(
                title=title,
                slug=slug,
                sku=sku,
                short_description=short_description,
                detail_description=detail_description,
                weight=weight,
                category_id=category_id,
                is_active=is_active,
                is_featured=is_featured,
                price=price  # Set price
            )
        elif product_data.get('diamond_product'):
            product = DiamondProduct.objects.create(
                title=title,
                slug=slug,
                sku=sku,
                detail_description=detail_description,
                weight=weight,
                category_id=category_id,
                is_active=is_active,
                is_featured=is_featured,
                price=price  # Set price
            )

    return product




# views for customization form 



def submit_inquiry(request):
    if request.method == 'POST':
        form = CustomizationInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:success')  # Redirect to a success page or any other page
    else:
        form = CustomizationInquiryForm()
    return render(request, 'submit_inquiry.html', {'form': form})


def order_placed(request):
    return render(request, 'store/order_placed.html')

def TC(request):
    return render(request,'store/terms.html')
    
def about_us(request):
     return render(request,'store/about_us.html') 
 
def helpcenter(request):
     return render(request,'store/helpcenter.html')  
 
def FAQ(request):
     return render(request,'store/FAQ.html')   
 

 



# from django.shortcuts import render, redirect
# from .utils import send_sms

# def notify_user(request):
#     # Example logic to retrieve phone numbers and message content
#     phone_numbers = [8129907709]  # Replace with actual user phone numbers
#     message = "Welcome to Subbaiya! Check out our latest offers."
    
#     # Call the send_sms function
#     response = send_sms(message, phone_numbers)
    
#     # Handle the response as needed
#     print(response)
    
#     return redirect('home') 



# from store.tasks import send_promotional_sms

# def trigger_sms(request):
#     send_promotional_sms.delay()  # Asynchronously send SMS
#     return redirect('some-view-name')
