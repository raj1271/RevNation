"""
URL configuration for RevNation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from RevApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.Index, name='home'),
    path("admindashboard/", views.dashboard, name='admindashboard'),
    path("manageproduct/", views.manageproduct, name='manageproduct'),
    path('usermanage/', views.usermanage, name='usermanage'),
    path('adminsetting/',views.adminsetting,name='adminsetting'),
    path('deleteuser/<str:EmailId>',views.deleteuser,name='deleteuser'),
    path('ordersadmin/',views.ordersadmin,name='ordersadmin'),
    path('about/',views.about,name='about'),
    path('shop/',views.shop,name='shop'),
    path('ShowReview/',views.ShowReview,name='ShowReview'),
    path('fullProduct/<str:category>/<int:product_id>/',views.fullProduct,name='fullProduct'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('addtocart/<str:category>/<int:product_id>/',views.addtocart,name='addtocart'),
    path('updateprice/<int:pid>/<int:q>/', views.updateprice, name='updateprice'),
    path('cart/', views.viewcart, name='cart'),
    path('cart/remove/<int:cart_id>/', views.removefromcart, name='removefromcart'),
    path('confirmorder/<str:totalprice>/',views.confirmorder,name='confirmorder'),
    path('confirmorder/<str:totalprice>/paymentsuccess',views.paymentsuccess,name='paymentsuccess'),
    path('homec/',views.cartdelete, name='homec'),
    path('faq/',views.Faq,name='faq'),
    path('regiuser/',views.RegiUser,name='regiuser'),
    path('login/',views.login,name='login'),
    path('forgpass/',views.forgpass,name='forgpass'),
    path('viewprof/',views.viewprof,name='viewprof'),
    path('Editprof/',views.Editprof,name='Editprof'),
    path('logout/',views.logout,name='logout'),
    path("addproduct/", views.Addproduct, name='addproduct'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
