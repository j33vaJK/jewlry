
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from decimal import Decimal


#For sending Messages through API ================>

class SendMessage(models.Model):
    text_message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)
    file = models.FileField(upload_to='message_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message sent on {self.created_at}"


class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    locality = models.CharField(max_length=150, verbose_name="House Name / House No")
    city = models.CharField(max_length=150, verbose_name="City")
    pin_code = models.CharField(max_length=10, verbose_name="Pincode")  # Adjust max_length as needed
    state = models.CharField(max_length=150, verbose_name="State")

    def __str__(self):
        return f"{self.locality}, {self.city}, {self.state} - {self.pin_code}"
    
# For Uploading Profile Image ==============>

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # New field for phone number

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.email}'


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="Category Image")
    is_active = models.BooleanField(verbose_name="Is Active?", default=0)
    is_featured = models.BooleanField(verbose_name="Is Featured?", default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title


class TodaysRate(models.Model):
    KARAT_CHOICES = [
        (18, '18 KT'),
        (22, '22 KT'),
        (24, '24 KT'),
    ]

    METAL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('diamond', 'Diamond'),
    ]

    metal = models.CharField(max_length=10, choices=METAL_CHOICES, verbose_name="Metal")
    karat = models.PositiveIntegerField(choices=KARAT_CHOICES, null=True, blank=True, verbose_name="Karat")
    rate = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Rate")
    date = models.DateField(default=timezone.now, verbose_name="Date")

    class Meta:
        verbose_name = "Today's Rate"
        verbose_name_plural = "Today's Rates"

    def __str__(self):
        return f"{self.date} - {self.metal} - {self.karat or ''} - {self.rate}"


# class GoldProduct(models.Model):
#     GOLD_CHOICES = [
#         ('na', 'N/A'),
#         ('rose_gold', 'Rose Gold'),
#         ('yellow_gold', 'Yellow Gold'),
#         ('white_gold', 'White Gold'),
#     ]
#     GOLD_ORNAMENT_CHOICES = [
#         ('na', 'N/A'),
#         ('gold_anklets', 'Gold Anklets'),
#         ('gold_baby_bangles', 'Gold Baby Bangles'),
#         ('gold_bangles', 'Gold Bangles'),
#         ('gold_bracelets', 'Gold Bracelets'),
#         ('gold_chains', 'Gold Chains'),
#         ('gold_ear_chains', 'Gold Ear Chains'),
#         ('gold_ear_rings', 'Gold Ear Rings'),
#         ('gold_ear_tops', 'Gold Ear Tops'),
#         ('gold_hip_chains', 'Gold Hip Chains'),
#         ('gold_necklaces', 'Gold Necklaces'),
#         ('gold_nose_pins', 'Gold Nose Pins'),
#         ('gold_pendants', 'Gold Pendants'),
#         ('gold_rings', 'Gold Rings'),
#         ('gold_special_items', 'Gold Special Items'),
#     ]
   
#     category = models.ForeignKey(Category, verbose_name="Product Category", on_delete=models.CASCADE)
#     title = models.CharField(max_length=150, verbose_name="Product Title")
#     slug = models.SlugField(max_length=160, verbose_name="Product Slug")
#     sku = models.CharField(max_length=255, unique=True, verbose_name="Unique Product ID (SKU)")
#     details = models.TextField(blank=True, null=True, verbose_name="Details")
#     gold = models.CharField(choices=GOLD_CHOICES, max_length=150, verbose_name="Gold Type")
#     gold_ornament_type = models.CharField(choices=GOLD_ORNAMENT_CHOICES, max_length=150, verbose_name="Gold Ornament Type")
#     karatage_choices = [
#         (18, '18 KT'),
#         (22, '22 KT'),
#     ]
#     karatage = models.PositiveIntegerField(choices=karatage_choices, null=True, blank=True, verbose_name="Karatage")
#     weight = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Weight (in grams)", default=0)
#     size = models.CharField(max_length=50, verbose_name="Size", default="Type the ornement size")
#     fixed_mrp_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     gold_rate = models.ForeignKey(TodaysRate, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Today's Rate")
#     # uses_fixed_mrp = models.BooleanField(default=False)
#     making_charges = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Making Charges / gram", default=1200)
#     gst_amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="GST Amount", default=0)
#     price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Gold Price")
#     total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Amount", default=0)
#     is_active = models.BooleanField(verbose_name="Is Active?")
#     is_featured = models.BooleanField(verbose_name="Is Featured?")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
#     discount = models.IntegerField(default=0, verbose_name="Discount (%)")



#     # def get_display_price(self):
#     #     if self.fixed_mrp_price:
#     #         return self.fixed_mrp_price
#     #     else:
#     #         return self.metal_price + self.making_charges + self.gst
    
#     # def get_display_price(self):
#     #     if self.uses_fixed_mrp and self.fixed_mrp_price:
#     #         return self.fixed_mrp_price
#     #     else:
#     #         return (self.gold_rate or 0) + (self.gst_amount or 0) + (self.making_charges or 0) 
        
        
#     def get_discounted_price(self):
#         discount_amount = self.total_amount * Decimal(self.discount / 100)
#         return self.total_amount - discount_amount

#     def update_price_based_on_gold_rate(self, gold_rate=None):
#         if gold_rate:
#             self.price = self.weight * gold_rate
#         elif self.gold_rate:
#             self.price = self.weight * self.gold_rate.rate

#     def calculate_total_amount(self):
#         return self.price + self.making_charges + self.gst_amount

#     def calculate_gst_amount(self):
#         total = self.price + self.making_charges
#         self.gst_amount = total * Decimal('0.03')


#     def save(self, *args, **kwargs):
#         self.update_price_based_on_gold_rate()
#         self.calculate_gst_amount()
#         self.total_amount = self.calculate_total_amount()
#         super(GoldProduct, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.title


class GoldProduct(models.Model):
    GOLD_CHOICES = [
        ('na', 'N/A'),
        ('rose_gold', 'Rose Gold'),
        ('yellow_gold', 'Yellow Gold'),
        ('white_gold', 'White Gold'),
    ]
    GOLD_ORNAMENT_CHOICES = [
        ('na', 'N/A'),
        ('gold_anklets', 'Gold Anklets'),
        ('gold_baby_bangles', 'Gold Baby Bangles'),
        ('gold_bangles', 'Gold Bangles'),
        ('gold_bracelets', 'Gold Bracelets'),
        ('gold_chains', 'Gold Chains'),
        ('gold_ear_chains', 'Gold Ear Chains'),
        ('gold_ear_rings', 'Gold Ear Rings'),
        ('gold_ear_tops', 'Gold Ear Tops'),
        ('gold_hip_chains', 'Gold Hip Chains'),
        ('gold_necklaces', 'Gold Necklaces'),
        ('gold_nose_pins', 'Gold Nose Pins'),
        ('gold_pendants', 'Gold Pendants'),
        ('gold_rings', 'Gold Rings'),
        ('gold_special_items', 'Gold Special Items'),
    ]

    category = models.ForeignKey(Category, verbose_name="Product Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name="Product Title")
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Unique Product ID (SKU)")
    details = models.TextField(blank=True, null=True, verbose_name="Details")
    gold = models.CharField(choices=GOLD_CHOICES, max_length=150, verbose_name="Gold Type")
    gold_ornament_type = models.CharField(choices=GOLD_ORNAMENT_CHOICES, max_length=150, verbose_name="Gold Ornament Type")
    karatage_choices = [
        (18, '18 KT'),
        (22, '22 KT'),
    ]
    karatage = models.PositiveIntegerField(choices=karatage_choices, null=True, blank=True, verbose_name="Karatage")
    weight = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Weight (in grams)", default=0)
    size = models.CharField(max_length=50, verbose_name="Size", default="Type the ornament size")
    fixed_mrp_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gold_rate = models.ForeignKey(TodaysRate, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Today's Rate")
    making_charges = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Making Charges / gram", default=1200)
    gst_amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="GST Amount", default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Gold Price")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Amount", default=0)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    discount = models.IntegerField(default=0, verbose_name="Discount (%)")
    
    def get_effective_price(self):
        if self.fixed_mrp_price:
            return self.fixed_mrp_price
        elif self.discount:
            return self.get_discounted_price()
        return self.total_amount

    def get_discounted_price(self):
        discount_amount = self.total_amount * Decimal(self.discount / 100)
        return self.total_amount - discount_amount

    def update_price_based_on_gold_rate(self, gold_rate=None):
        if not self.fixed_mrp_price:
            if gold_rate:
                self.price = self.weight * gold_rate
            elif self.gold_rate:
                self.price = self.weight * self.gold_rate.rate
        else:
            self.price = self.fixed_mrp_price

    def calculate_total_amount(self):
        if self.fixed_mrp_price:
            return self.fixed_mrp_price
        else:
            return self.price + self.making_charges + self.gst_amount

    def calculate_gst_amount(self):
        if not self.fixed_mrp_price:
            total = self.price + self.making_charges
            self.gst_amount = total * Decimal('0.03')

    def save(self, *args, **kwargs):
        self.update_price_based_on_gold_rate()
        self.calculate_gst_amount()
        self.total_amount = self.calculate_total_amount()
        super(GoldProduct, self).save(*args, **kwargs)

    def __str__(self):
        return self.title





class SilverProduct(models.Model):
    SILVER_CHOICES = [
        ('sterling_silver', 'Sterling Silver'),
        ('pure_silver', 'Pure Silver'),
    ]
    SILVER_ORNAMENT_CHOICES = [
        ('silver_anklets', 'Silver Anklets'),
        ('silver_bangles', 'Silver Bangles'),
        ('silver_bracelets', 'Silver Bracelets'),
        ('silver_chains', 'Silver Chains'),
        ('silver_necklaces', 'Silver Necklaces'),
        ('silver_lamps', 'Silver Lamps'),
        ('silver_vessels', 'Silver Vessels'),
    ]
    category = models.ForeignKey(Category, verbose_name="Product Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name="Product Title")
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Unique Product ID (SKU)")
    details = models.TextField(blank=True, null=True, verbose_name="Details")
    silver_type = models.CharField(choices=SILVER_CHOICES, max_length=150, verbose_name="Silver Type")
    silver_ornament_type = models.CharField(choices=SILVER_ORNAMENT_CHOICES, max_length=150, verbose_name="Silver Ornament Type")
    screw_choices = [
        ('N/A', 'N/A'),
        ('south_screw', 'South screw'),
        ('regular_screw', 'Regular screw'),
    ]
    screw = models.CharField(max_length=100, choices= screw_choices, null=True, blank=True, verbose_name="Screw type")
    karatage_choices = [
        ('N/A', 'N/A'),
        ('925', '925'),
    ]
    karatage = models.CharField(max_length=10, choices=karatage_choices, null=True, blank=True, verbose_name="Karatage")
    weight = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Weight (in grams)", default=0)
    size = models.CharField(max_length=50, verbose_name="Size", default="Type the ornement size")
    fixed_mrp_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    making_charges = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Making Charges / gram", default=1200)
    gst_amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="GST Amount", default=0)
    gold_rate = models.ForeignKey(TodaysRate, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Today's Rate")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Amount", default=0)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    discount = models.IntegerField(default=0, verbose_name="Discount (%)")
    
    def get_effective_price(self):
        if self.fixed_mrp_price:
            return self.fixed_mrp_price
        elif self.discount:
            return self.get_discounted_price()
        return self.total_amount

    def get_discounted_price(self):
        discount_amount = self.total_amount * Decimal(self.discount / 100)
        return self.total_amount - discount_amount

    def update_price_based_on_gold_rate(self, gold_rate=None):
        if gold_rate:
            self.price = self.weight * gold_rate
        elif self.gold_rate:
            self.price = self.weight * self.gold_rate.rate

    def calculate_gst_amount(self):
        total = self.price + self.making_charges
        self.gst_amount = total * Decimal('0.03')

    def calculate_total_amount(self):
        return self.price + self.making_charges + self.gst_amount

    def save(self, *args, **kwargs):
        self.update_price_based_on_gold_rate()
        self.calculate_gst_amount()
        self.total_amount = self.calculate_total_amount()
        super(SilverProduct, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class DiamondProduct(models.Model):
    DIAMOND_ORNAMENT_CHOICES = [
        ('diamond_bangles', 'Diamond Bangles'),
        ('diamond_bracelets', 'Diamond Bracelets'),
        ('diamond_chains', 'Diamond Chains'),
        ('diamond_ear_rings', 'Diamond Ear Rings'),
        ('diamond_necklaces', 'Diamond Necklaces'),
        ('diamond_nose_pins', 'Diamond Nose Pins'),
        ('diamond_pendants', 'Diamond Pendants'),
        ('diamond_rings', 'Diamond Rings'),
        ('diamond_special_items', 'Diamond Special Items'),
    ]

    
    
    DIAMOND_QUALITY_CHOICES = [
        ('VVS', 'VVS'),
        ('1VVS 2', '1VVS 2'),
        ('SI', 'SI'),
    ]

    GOLD_CHOICES = [
        ('na', 'N/A'),
        ('rose_gold', 'Rose Gold'),
        ('yellow_gold', 'Yellow Gold'),
        ('white_gold', 'White Gold'),
    ]

    category = models.ForeignKey(Category, verbose_name="Product Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name="Product Title")
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Unique Product ID (SKU)")
    details = models.TextField(blank=True, null=True, verbose_name="Details")
    diamond_ornament_type = models.CharField(choices=DIAMOND_ORNAMENT_CHOICES, max_length=150, verbose_name="Diamond Ornament Type")
    karatage_choices = [
        (18, '18 KT'),
        (22, '22 KT'),
    ]
    diamond_quantity = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Diamond Quantity", default=0)
    diamond_color = models.CharField(max_length=50, verbose_name="Diamond Color", default="Type your color")
    diamond_quality = models.CharField(choices=DIAMOND_QUALITY_CHOICES, max_length=150, verbose_name="Diamond Quality", blank=True, null=True)
    carats = models.DecimalField(max_digits=8, decimal_places=5, verbose_name="Carats (Ct)", default=0)
    diamond_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Diamond Price", default=0)  # New field
    karatage = models.PositiveIntegerField(choices=karatage_choices, null=True, blank=True, verbose_name="Gold Karatage")
    fixed_mrp_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gold = models.CharField(choices=GOLD_CHOICES, max_length=150, verbose_name="Gold Color")
    weight = models.DecimalField(max_digits=8, decimal_places=5, verbose_name="Gold Weight (grams)", default=0)
    size = models.CharField(max_length=50, verbose_name="Size", default="Type the ornement size")
    gross_weight = models.DecimalField(max_digits=8, decimal_places=5, null=True, verbose_name="Gross Weight (grams)", default=0)
    making_charges = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Making Charges / gram", default=1200)
    gst_amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="GST Amount", default=0)
    gold_rate = models.ForeignKey(TodaysRate, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Today's Rate")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Amount", default=0)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    discount = models.IntegerField(default=0, verbose_name="Discount (%)")

    # def get_discounted_price(self):
    #     discount_amount = self.total_amount * Decimal(self.discount / 100)
    #     return self.total_amount - discount_amount


    # def calculate_gross_weight(self):
    #     carat_in_grams = self.carats * Decimal('0.2')
    #     self.gross_weight = carat_in_grams + self.weight

    # def update_price_based_on_gold_rate(self, gold_rate=None):
    #     if gold_rate:
    #         self.price = self.weight * gold_rate
    #     elif self.gold_rate:
    #         self.price = self.weight * self.gold_rate.rate

    # def calculate_gst_amount(self):
    #     total = self.price + self.making_charges + self.diamond_price  # Include diamond_price
    #     self.gst_amount = total * Decimal('0.03')

    # def calculate_total_amount(self):
    #     return self.price + self.making_charges + self.gst_amount + self.diamond_price

    # def save(self, *args, **kwargs):
    #     self.diamond_price = self.carats * Decimal('125000')  # Calculate diamond_price
    #     self.update_price_based_on_gold_rate()
    #     self.calculate_gst_amount()
    #     self.calculate_gross_weight()
    #     self.total_amount = self.calculate_total_amount()
    #     super(DiamondProduct, self).save(*args, **kwargs)

    # def __str__(self):
    #     return self.title

    def get_effective_price(self):
        if self.fixed_mrp_price:
            return self.fixed_mrp_price
        elif self.discount:
            return self.get_discounted_price()
        return self.total_amount

    def get_discounted_price(self):
        discount_amount = self.total_amount * Decimal(self.discount / 100)
        return self.total_amount - discount_amount

    def calculate_gross_weight(self):
        carat_in_grams = self.carats * Decimal('0.2')
        self.gross_weight = carat_in_grams + self.weight

    def update_price_based_on_gold_rate(self, gold_rate=None):
        if gold_rate:
            self.price = self.weight * gold_rate
        elif self.gold_rate:
            self.price = self.weight * self.gold_rate.rate

    def calculate_gst_amount(self):
        total = self.price + self.making_charges + self.diamond_price  # Include diamond_price
        self.gst_amount = total * Decimal('0.03')

    def calculate_total_amount(self):
        return self.price + self.making_charges + self.gst_amount + self.diamond_price

    def save(self, *args, **kwargs):
        self.diamond_price = self.carats * Decimal('125000')  # Calculate diamond_price
        self.update_price_based_on_gold_rate()
        self.calculate_gst_amount()
        self.calculate_gross_weight()
        self.total_amount = self.calculate_total_amount()
        super(DiamondProduct, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

@receiver(pre_save, sender=GoldProduct)
def update_gold_product_price(sender, instance, **kwargs):
    instance.update_price_based_on_gold_rate()


@receiver(pre_save, sender=SilverProduct)
def update_silver_product_price(sender, instance, **kwargs):
    instance.update_price_based_on_gold_rate()


@receiver(pre_save, sender=DiamondProduct)
def update_diamond_product_price(sender, instance, **kwargs):
    instance.update_price_based_on_gold_rate()


@receiver(post_save, sender=TodaysRate)
def update_product_prices_on_todays_rate_change(sender, instance, created, **kwargs):
    if not created:
        gold_products = GoldProduct.objects.filter(gold_rate=instance)
        for product in gold_products:
            product.update_price_based_on_gold_rate(instance.rate)
            product.save()

        silver_products = SilverProduct.objects.filter(gold_rate=instance)
        for product in silver_products:
            product.update_price_based_on_gold_rate(instance.rate)
            product.save()

        diamond_products = DiamondProduct.objects.filter(gold_rate=instance)
        for product in diamond_products:
            product.update_price_based_on_gold_rate(instance.rate)
            product.save()

class GiftProduct(models.Model):
    GIFT_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
    ]
    
    # Select the type of product associated with the gift
    product_type = models.CharField(choices=GIFT_CHOICES, max_length=10, verbose_name="Product Type")
    
    # Foreign key fields to GoldProduct and SilverProduct
    gold_product = models.ForeignKey(GoldProduct, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Gold Product")
    silver_product = models.ForeignKey(SilverProduct, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Silver Product")
    
    # Common fields
    title = models.CharField(max_length=150, verbose_name="Gift Title")
    slug = models.SlugField(max_length=160, verbose_name="Gift Slug")
    details = models.TextField(blank=True, null=True, verbose_name="Details")
    image = models.ImageField(upload_to='gift_images/', verbose_name="Image")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price")
    is_active = models.BooleanField(verbose_name="Is Active?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def save(self, *args, **kwargs):
        # Set the price based on the associated product type
        if self.product_type == 'gold' and self.gold_product:
            self.price = self.gold_product.price
        elif self.product_type == 'silver' and self.silver_product:
            self.price = self.silver_product.price
        super(GiftProduct, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class ProductImage(models.Model):
    # ForeignKey fields for each type of product
    gold_product = models.ForeignKey(GoldProduct, related_name='images', verbose_name="Gold Product", on_delete=models.CASCADE, null=True, blank=True)
    silver_product = models.ForeignKey(SilverProduct, related_name='images', verbose_name="Silver Product", on_delete=models.CASCADE, null=True, blank=True)
    diamond_product = models.ForeignKey(DiamondProduct, related_name='images', verbose_name="Diamond Product", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='product_images', verbose_name="Product Image")
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name="Uploaded Date")

    def __str__(self):
        return f"Image for {self.gold_product or self.silver_product or self.diamond_product}"

class CarousalImage(models.Model):
    name = models.CharField(max_length=255, default='Carousal Image')
    carousal_image = models.ImageField(upload_to='carousal_images', verbose_name="Carousal Image")
    uploaded_time = models.DateTimeField(default=timezone.now, verbose_name="Uploaded Time")
    
    def __str__(self):
        return self.name

class Specials(models.Model):
    name = models.CharField(max_length=255, default='Special Image')
    special_image = models.ImageField(upload_to='special_images', verbose_name="Special Image")
    uploaded_time = models.DateTimeField(default=timezone.now, verbose_name="Uploaded Time")
    
    def __str__(self):
        return self.name

# class Cart(models.Model):
#     user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
#     gold_product = models.ForeignKey(GoldProduct, verbose_name="Gold Product", on_delete=models.CASCADE, null=True, blank=True)
#     silver_product = models.ForeignKey(SilverProduct, verbose_name="Silver Product", on_delete=models.CASCADE, null=True, blank=True)
#     diamond_product = models.ForeignKey(DiamondProduct, verbose_name="Diamond Product", on_delete=models.CASCADE, null=True, blank=True)
#     quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

#     def __str__(self):
#         return f"{self.user.username}'s cart"



class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    gold_product = models.ForeignKey(GoldProduct, verbose_name="Gold Product", on_delete=models.CASCADE, null=True, blank=True)
    silver_product = models.ForeignKey(SilverProduct, verbose_name="Silver Product", on_delete=models.CASCADE, null=True, blank=True)
    diamond_product = models.ForeignKey(DiamondProduct, verbose_name="Diamond Product", on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    admin_message = models.TextField(blank=True, null=True, verbose_name="Admin Message")

    def __str__(self):
        return f"{self.user.username}'s cart"

    @property
    def effective_price(self):
        """
        Get the effective price per item considering fixed MRP, discount, or total amount.
        """
        if self.gold_product:
            return self.gold_product.get_effective_price()
        elif self.silver_product:
            return self.silver_product.get_effective_price()
        elif self.diamond_product:
            return self.diamond_product.get_effective_price()
        return Decimal('0')

    @property
    def total_price(self):
        """
        Calculate the total price based on quantity and effective price.
        """
        return self.quantity * self.effective_price
    
# original below    

# class Cart(models.Model):
#     user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
#     gold_product = models.ForeignKey(GoldProduct, verbose_name="Gold Product", on_delete=models.CASCADE, null=True, blank=True)
#     silver_product = models.ForeignKey(SilverProduct, verbose_name="Silver Product", on_delete=models.CASCADE, null=True, blank=True)
#     diamond_product = models.ForeignKey(DiamondProduct, verbose_name="Diamond Product", on_delete=models.CASCADE, null=True, blank=True)
#     quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

#     def __str__(self):
#         return f"{self.user.username}'s cart"

#     @property
#     def effective_price(self):
#         """
#         Get the effective price per item considering fixed MRP, discount, or total amount.
#         """
#         if self.gold_product:
#             return self.gold_product.get_effective_price()
#         elif self.silver_product:
#             return self.silver_product.get_effective_price()
#         elif self.diamond_product:
#             return self.diamond_product.get_effective_price()
#         return Decimal('0')

#     @property
#     def total_price(self):
#         """
#         Calculate the total price based on quantity and effective price.
#         """
#         return self.quantity * self.effective_price


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)


class Wishlist(models.Model):
    user = models.ForeignKey(User,verbose_name="user", on_delete=models.CASCADE)
    gold_products = models.ManyToManyField(GoldProduct,verbose_name="Gold Product", blank=True)
    silver_products = models.ManyToManyField(SilverProduct, verbose_name="Silver Product", blank=True)
    diamond_products = models.ManyToManyField(DiamondProduct,verbose_name="Diamond Product", blank=True)

    def __str__(self):
        return f"Wishlist for {self.user}"


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Shipping Address", on_delete=models.CASCADE)
    gold_product = models.ForeignKey(GoldProduct, verbose_name="Gold Product", on_delete=models.CASCADE, null=True, blank=True)
    silver_product = models.ForeignKey(SilverProduct, verbose_name="Silver Product", on_delete=models.CASCADE, null=True, blank=True)
    diamond_product = models.ForeignKey(DiamondProduct, verbose_name="Diamond Product", on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="Pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    

    @property   
    def total_price(self):
        if self.gold_product:
            return self.quantity * self.gold_product.price
        elif self.silver_product:
            return self.quantity * self.silver_product.price
        elif self.diamond_product:
            return self.quantity * self.diamond_product.price
        return 0
    


# customization for the customer


class CustomizationInquiry(models.Model):
    name = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    admin_remarks = models.TextField(blank=True, null=True)
    # Checkbox field to indicate if an order has been placed 
    has_placed_order = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.product_name}"


# This model will store different types of messages your client wants to send.
# class MessageTemplate(models.Model):
#     title = models.CharField(max_length=255, verbose_name="Title")
#     content = models.TextField(verbose_name="Content")
#     is_active = models.BooleanField(default=True, verbose_name="Active")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

#     def __str__(self):
#         return self.title

# # This model will track messages sent to users, including whether they were successfully delivered.
# class MessageLog(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
#     message_template = models.ForeignKey(MessageTemplate, on_delete=models.SET_NULL, null=True, verbose_name="Message Template")
#     content = models.TextField(verbose_name="Message Content")
#     sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Sent Date")
#     status = models.CharField(max_length=50, verbose_name="Status")
#     error_message = models.TextField(blank=True, null=True, verbose_name="Error Message")

#     def __str__(self):
#         return f"Message to {self.user.username} on {self.sent_at}"
