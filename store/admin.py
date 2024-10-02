from django.contrib import admin

from store.utils import fetch_phone_numbers, send_whatsapp_message
from.models import SendMessage, Wishlist
from .models import CustomizationInquiry
# from .utils import send_admin_message
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Order
# from .models import MessageTemplate, MessageLog
from .models import (
    Address, Category, GoldProduct, SilverProduct, DiamondProduct,
    Cart, Order, ProductImage, CarousalImage, ContactSubmission, Specials, TodaysRate, GiftProduct,Profile
)



@admin.register(SendMessage)
class SendMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        print("save_model triggered")
        super().save_model(request, obj, form, change)
        """
        Custom behavior after the admin clicks the save button (to send the message).
        """
        # Fetch all phone numbers of registered users
        phone_numbers = fetch_phone_numbers()

        # Construct the message to send
        text_message = obj.text_message

        # file_url = None

        if obj.image:
            image_url = request.build_absolute_uri(obj.image.url)
           
        # if obj.file:
        #     file_url = request.build_absolute_uri(obj.file.url)
        
        # Call the WhatsApp API function (modify the function to handle text, image, and file)
        send_whatsapp_message(
            apikey='e45c575504914d1e982df8674958864a',
            mobile_numbers=phone_numbers,
            text_message=text_message,
            image_url=image_url,
            # file_url=file_url
        )

        # Optionally, you can show a message to the admin after sending
        self.message_user(request, f"Message sent to {len(phone_numbers)} users!")

        return super().response_change(request, obj)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email')


class TodaysRateAdmin(admin.ModelAdmin):
    list_display = ('metal', 'karat', 'rate', 'date')
    list_filter = ('metal', 'karat', 'date')
    search_fields = ('rate',)
    date_hierarchy = 'date'

    def get_queryset(self, request):
        # Filter to show only today's rates by default
        queryset = super().get_queryset(request)
        if request.GET.get('metal'):
            metal = request.GET['metal']
            queryset = queryset.filter(metal=metal)
        return queryset

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['gold_url'] = self.get_admin_url('gold')
        extra_context['silver_url'] = self.get_admin_url('silver')
        extra_context['diamond_url'] = self.get_admin_url('diamond')
        return super().changelist_view(request, extra_context=extra_context)

    def get_admin_url(self, metal):
        # Generate URL for filtering by metal type
        return f"admin/{self.model._meta.app_label}/{self.model._meta.model_name}/?metal={metal}"



# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'locality', 'city', 'state')
    list_filter = ('city', 'state')
    list_per_page = 10
    search_fields = ('locality', 'city', 'state')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title", )}

class GoldProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 'category', 'display_product_image',
        'is_active', 'is_featured', 'updated_at'
    )
    list_editable = ('slug', 'category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'category__title', 'short_description')
    prepopulated_fields = {"slug": ("title", )}

    def display_product_image(self, obj):
        if obj.images.exists():
            return obj.images.first().image.url
        return 'No Image'
    
    display_product_image.short_description = 'Product Image'

class SilverProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 'category', 'display_product_image',
        'is_active', 'is_featured', 'updated_at'
    )
    list_editable = ('slug', 'category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'category__title', 'short_description')
    prepopulated_fields = {"slug": ("title", )}

    def display_product_image(self, obj):
        if obj.images.exists():
            return obj.images.first().image.url
        return 'No Image'
    
    display_product_image.short_description = 'Product Image'

class DiamondProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'display_product_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'category__title', 'short_description',)
    prepopulated_fields = {"slug": ("title", )}
    
    def display_product_image(self, obj):
        if obj.images.exists():
            return obj.images.first().image.url
        return 'No Image'
    
    display_product_image.short_description = 'Product Image'  # Set column header name


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_product_title', 'quantity', 'created_at', 'admin_message')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user__username', 'gold_product__title', 'silver_product__title', 'diamond_product__title')
    actions = ['send_message']

    def get_product_title(self, obj):
        if obj.gold_product:
            return obj.gold_product.title
        elif obj.silver_product:
            return obj.silver_product.title
        elif obj.diamond_product:
            return obj.diamond_product.title
        return 'No Product'
    
    get_product_title.short_description = 'Product Title'

    def send_message(self, request, queryset):
        for cart in queryset:
            send_admin_message(cart.id)
        self.message_user(request, "Messages sent successfully.")

    send_message.short_description = "Send Message to Selected Customers"

 
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Display the user associated with the wishlist
    filter_horizontal = ('gold_products', 'silver_products', 'diamond_products')  # Allow multi-select in the admin interface
    search_fields = ('user__username',)




class ProductTypeFilter(admin.SimpleListFilter):
    title = 'Product Type'
    parameter_name = 'product_type'

    def lookups(self, request, model_admin):
        return (
            ('gold', 'Gold Products'),
            ('silver', 'Silver Products'),
            ('diamond', 'Diamond Products'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'gold':
            return queryset.filter(gold_product__isnull=False)
        if self.value() == 'silver':
            return queryset.filter(silver_product__isnull=False)
        if self.value() == 'diamond':
            return queryset.filter(diamond_product__isnull=False)
        return queryset

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_title', 'quantity', 'status', 'ordered_date')
    list_editable = ('quantity', 'status')
    list_filter = ('status', 'ordered_date', ProductTypeFilter)
    list_per_page = 20
    search_fields = ('user__username', 'gold_product__title', 'silver_product__title', 'diamond_product__title')

    def product_title(self, obj):
        if obj.gold_product:
            return obj.gold_product.title
        elif obj.silver_product:
            return obj.silver_product.title
        elif obj.diamond_product:
            return obj.diamond_product.title
        return 'No Product'

    product_title.short_description = 'Product Title'




class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'image', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('gold_product__title', 'silver_product__title', 'diamond_product__title')  # Search by product title

    def product_title(self, obj):
        return obj.gold_product.title if obj.gold_product else (obj.silver_product.title if obj.silver_product else obj.diamond_product.title)
    
    product_title.short_description = 'Product Title'


class GiftProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'product_type', 'price', 'is_active')
    search_fields = ('title', 'product_type')
    list_filter = ('product_type', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('gold_product', 'silver_product')
    
    
class CustomizationInquiryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'product_name', 'email', 'mobile', 'created_at', 'has_placed_order']
    search_fields = ['name', 'product_name', 'email', 'mobile']
    # list_filter = ('inquiry_type', 'created_at', 'has_placed_order')
    # search_fields = ('user__username', 'inquiry_type')
    actions = ['export_inquiries']

    def export_inquiries(self, request, queryset):
        # Add your export logic here if needed, but ImportExportModelAdmin handles it automatically.
        pass

    export_inquiries.short_description = "Export Selected Inquiries"

    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')  # Display user and phone number in the admin list



admin.site.register(Address, AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(GoldProduct, GoldProductAdmin)
admin.site.register(SilverProduct, SilverProductAdmin)
admin.site.register(DiamondProduct, DiamondProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(TodaysRate, TodaysRateAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(CarousalImage)
admin.site.register(Specials)
admin.site.register(GiftProduct, GiftProductAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(CustomizationInquiry,CustomizationInquiryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Profile, ProfileAdmin)