from django.contrib import admin
from .models import UserModel,AdminModel,Helmet, Jacket, Gloves, Boots, RidingPants, Kneeguard, FAQModel,Cart,Order,Payment,OrderItem

# Register your models here.
admin.site.register(UserModel)
admin.site.register(AdminModel)
admin.site.register(FAQModel)
admin.site.register(Helmet)
admin.site.register(Jacket)
admin.site.register(Gloves)
admin.site.register(Boots)
admin.site.register(Kneeguard)
admin.site.register(RidingPants)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderItem)