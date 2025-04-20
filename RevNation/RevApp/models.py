from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

# User Model
class UserModel(models.Model):
    FirstName=models.CharField(max_length=100,null=False)
    LastName=models.CharField(max_length=100,null=False)
    EmailId=models.CharField(max_length=100,null=False,primary_key=True)
    PhoneNo=models.CharField(max_length=100,null=False,unique=True)
    Password=models.CharField(max_length=100,null=False)
    DOB=models.CharField(max_length=100,null=False)
    Gender=models.CharField(max_length=100,null=False)
    StreetAddress=models.CharField(max_length=100,null=False)
    City=models.CharField(max_length=100,null=False)
    State=models.CharField(max_length=100,null=False)
    Country=models.CharField(max_length=100)
    PinCode=models.CharField(max_length=100,null=False)

# Admin Model
class AdminModel(models.Model):
    adminEmailId=models.CharField(max_length=100,primary_key=True)
    adminPassword=models.CharField(max_length=100,null=False)
    adminName=models.CharField(max_length=100)
    adminPhoneno=models.CharField(max_length=20,null=False)

class forgetpassword(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    user_admin = models.ForeignKey(AdminModel, on_delete=models.CASCADE)
    otp=models.IntegerField()


# Base Product Model (Common Fields)
class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_availability = models.CharField(max_length=20, choices=[('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock')])
    image = models.ImageField(upload_to='product_images/')

    class Meta:
        abstract = True  # This makes it a base class, not stored in DB

    def __str__(self):
        return self.name


# Helmet Model
class Helmet(Product):
    TYPE_CHOICES = [('Full Face', 'Full Face'), ('Open Face', 'Open Face'), ('Modular', 'Modular'), ('Off-Road', 'Off-Road')]
    CERT_CHOICES = [('DOT', 'DOT'), ('ECE', 'ECE'), ('ISI', 'ISI'), ('DOT,ECE', 'DOT,ECE'), ('DOT,ISI', 'DOT,ISI'), ('DOT,ECE,ISI', 'DOT,ECE,ISI')]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    certifications = models.CharField(max_length=50, choices=CERT_CHOICES)
    size = models.CharField(max_length=10, choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')])
    color = models.CharField(max_length=50)


# Jacket Model
class Jacket(Product):
    TYPE_CHOICES = [('Off-Road', 'Off-Road'), ('Racing', 'Racing'), ('Adventure', 'Adventure'), ('Winter', 'Winter')]
    MATE_CHOICES = [('Leather', 'Leather'), ('Textile', 'Textile'), ('Mesh', 'Mesh')]
    

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    size = models.CharField(max_length=10, choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')])
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100, choices=MATE_CHOICES)
    certifications = models.CharField(max_length=50)
    reflective_elements = models.BooleanField(default=False)
    ventilation_system = models.CharField(max_length=100, null=True, blank=True)
    padding_protection = models.CharField(max_length=255, null=True, blank=True)
    waterproofing = models.BooleanField(default=False)


# Gloves Model
class Gloves(Product):
    TYPE_CHOICES = [('Full Gauntlet', 'Full Gauntlet'), ('Short Cuff', 'Short Cuff'), ('Winter', 'Winter'), ('Racing', 'Racing'), ('Adventure', 'Adventure')]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    size = models.CharField(max_length=10, choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')])
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    certifications = models.CharField(max_length=50)
    waterproofing = models.BooleanField(default=False)
    touchscreen_compatibility = models.BooleanField(default=False)


# Boots Model
class Boots(Product):
    TYPE_CHOICES = [('Touring', 'Touring'), ('Racing', 'Racing'), ('Adventure', 'Adventure')]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    size = models.CharField(max_length=10, choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')])
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    certifications = models.CharField(max_length=50)
    closure_type = models.CharField(max_length=50, choices=[('Velcro', 'Velcro'), ('Zipper', 'Zipper'), ('Lace-up', 'Lace-up')])
    waterproofing = models.BooleanField(default=False)

# Kneeguard Model
class Kneeguard(Product):
    PROTECTION_LEVEL_CHOICES = [('CE Level 1', 'CE Level 1'), ('CE Level 2', 'CE Level 2')]

    protection_level = models.CharField(max_length=50, choices=PROTECTION_LEVEL_CHOICES)
    adjustable_straps = models.BooleanField(default=False)
    material = models.CharField(max_length=100)


# Riding Pants Model
class RidingPants(Product):
    TYPE_CHOICES = [('Off-Road', 'Off-Road'), ('Racing', 'Racing'), ('Adventure', 'Adventure'), ('Winter', 'Winter')]
    MATE_CHOICES = [('Leather', 'Leather'), ('Textile', 'Textile'), ('Mesh', 'Mesh')]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    size = models.CharField(max_length=10, choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')])
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100, choices=MATE_CHOICES)
    certifications = models.CharField(max_length=50)
    reflective_elements = models.BooleanField(default=False)
    ventilation_system = models.CharField(max_length=100, null=True, blank=True)
    padding_protection = models.CharField(max_length=255, null=True, blank=True)
    waterproofing = models.BooleanField(default=False)


class FAQModel(models.Model):
    emailId=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    question=models.CharField(max_length=500)
    ans=models.CharField(max_length=500)


class Review(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # Connects to User
    helmet = models.ForeignKey(Helmet, on_delete=models.CASCADE, null=True, blank=True)  # Connects to Helmet
    jacket = models.ForeignKey(Jacket, on_delete=models.CASCADE, null=True, blank=True)  # Connects to Jacket
    gloves = models.ForeignKey(Gloves, on_delete=models.CASCADE, null=True, blank=True)  # Connects to Gloves
    boots = models.ForeignKey(Boots, on_delete=models.CASCADE, null=True, blank=True)  # Connects to Boots
    kneeguard = models.ForeignKey(Kneeguard, on_delete=models.CASCADE, null=True, blank=True)  # Connects to Kneeguard
    ridingPants = models.ForeignKey(RidingPants, on_delete=models.CASCADE, null=True, blank=True)  # Connects to RidingPants
    rating = models.PositiveIntegerField(choices=[(1, "★☆☆☆☆"), (2, "★★☆☆☆"), (3, "★★★☆☆"), (4, "★★★★☆"), (5, "★★★★★")])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.helmet:
            return f"Review by {self.user.FirstName} for {self.helmet.name} - {self.rating} Stars"
        elif self.jacket:
            return f"Review by {self.user.FirstName} for {self.jacket.name} - {self.rating} Stars"
        elif self.gloves:
            return f"Review by {self.user.FirstName} for {self.gloves.name} - {self.rating} Stars"
        elif self.boots:
            return f"Review by {self.user.FirstName} for {self.boots.name} - {self.rating} Stars"
        elif self.kneeguard:
            return f"Review by {self.user.FirstName} for {self.kneeguard.name} - {self.rating} Stars"
        elif self.ridingPants:
            return f"Review by {self.user.FirstName} for {self.ridingPants.name} - {self.rating} Stars"
        

class Cart(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    helmet = models.ForeignKey(Helmet, on_delete=models.CASCADE, null=True, blank=True)
    jacket = models.ForeignKey(Jacket, on_delete=models.CASCADE, null=True, blank=True)
    gloves = models.ForeignKey(Gloves, on_delete=models.CASCADE, null=True, blank=True)
    boots = models.ForeignKey(Boots, on_delete=models.CASCADE, null=True, blank=True)
    kneeguard = models.ForeignKey(Kneeguard, on_delete=models.CASCADE, null=True, blank=True)
    riding_pants = models.ForeignKey(RidingPants, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        product = self.get_product()
        return self.quantity * product.price if product else 0

    def get_product(self):
        return self.helmet or self.jacket or self.gloves or self.boots or self.kneeguard or self.riding_pants

    def __str__(self):
        product = self.get_product()
        return f"{self.user.FirstName} - {product.name} ({self.quantity})" if product else "Empty Cart"




class Order(models.Model):

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    orderNo=models.CharField(max_length=100)
    StreetAddress=models.CharField(max_length=100,null=False)
    City=models.CharField(max_length=100,null=False)
    State=models.CharField(max_length=100,null=False)
    Country=models.CharField(max_length=100)
    PinCode=models.CharField(max_length=100,null=False)
    TotalBill=models.FloatField(default=0.0)
    
    payment_status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid')

    def __str__(self):
        return f"Order {self.id} - {self.user.FirstName}"
    
    class Meta:
        ordering = ['-created_at']  # Orders will be sorted by creation date, newest first


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")  # ✅ Fixed Relationship
    product_name = models.CharField(max_length=255)
    product_price = models.FloatField()
    product_image = models.ImageField(upload_to="order_items/", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"

class Payment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100, unique=True)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Completed')  # You can add more statuses if needed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.user.EmailId}"