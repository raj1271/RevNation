from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
import razorpay
from django.urls import reverse
from django.db.models import Prefetch
from datetime import date
from django.db.models import Sum
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import Http404, HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from .models import UserModel,AdminModel,Helmet,Jacket,Gloves,Boots,Kneeguard,RidingPants,FAQModel,Cart,Order,Payment,OrderItem

PRODUCT_MODELS = {
    'helmet': Helmet,
    'jacket': Jacket,
    'gloves': Gloves,
    'boots': Boots,
    'riding_pants': RidingPants,
    'knee_guard': Kneeguard
}
# Create your views here.

# Index View
def Index(request):
    helmets = Helmet.objects.all()
    return render(request,'index.html', {'helmets':helmets})

# About View
def about(request):
    return render(request,'about.html')

# Shop View
def shop(request):
    helmets = Helmet.objects.all()
    jackets = Jacket.objects.all()
    gloves = Gloves.objects.all()
    boots = Boots.objects.all()
    ridingpant = RidingPants.objects.all()
    kneeguard = Kneeguard.objects.all()
    
    return render(request, 'shop.html', {'helmets':helmets , 'jackets':jackets ,'gloves':gloves ,'boots':boots ,'ridingpant':ridingpant ,'kneeguard':kneeguard})

def fullProduct(request, category, product_id):
    model = PRODUCT_MODELS.get(category)
    product = get_object_or_404(model, id=product_id)
    context = {
        'product': product,
        'category': category
    }
    if request.method == "POST":
        pass
    else:
        return render(request, 'fullProduct.html', context)    

# manageproduct View
def manageproduct(request):
    helmets = Helmet.objects.all()
    jackets = Jacket.objects.all()
    gloves = Gloves.objects.all()
    boots = Boots.objects.all()
    ridingpant = RidingPants.objects.all()
    kneeguard = Kneeguard.objects.all()
    return render(request,'manageproduct.html',{'helmets':helmets , 'jackets':jackets ,'gloves':gloves ,'boots':boots ,'ridingpant':ridingpant ,'kneeguard':kneeguard})

# cart View
def viewcart(request): 
    cart_items = Cart.objects.filter(user=request.session['user_emailId'])
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

# add to cart
def addtocart(request,category, product_id):
    flag='Cart Added'
    direct=reverse('shop')
    category=category.lower()
    emailid=request.session['user_emailId']
    cust=UserModel.objects.get(EmailId=emailid)
    model = PRODUCT_MODELS.get(category)
    if model is None:
        raise Http404("Product category not found.")  # Handle invalid category

    product = get_object_or_404(model, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=cust,
        **{category: product}  # Assign the specific product type
    )
    if not created:
        cart_item.quantity += 1  # Increment quantity if already in cart
        cart_item.save()
    return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}}) 

# Update price
def updateprice(request, pid, q):
    cart_data=Cart.objects.filter(id=pid)
    cart_data.update(quantity=q)
    return redirect('cart')

# remove from cart
def removefromcart(request, cart_id,):
    flag='Cart Item Deleted'
    direct=reverse('cart')
    emailid=request.session['user_emailId']
    cart_item = get_object_or_404(Cart, id=cart_id, user=emailid)
    cart_item.delete()
    return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}}) 

# ConfirmOrder View
def confirmorder(request,totalprice):
    tprice=float(totalprice)
    emailid=request.session['user_emailId']
    cust = get_object_or_404(UserModel, EmailId=emailid)
    if request.method == "POST":
        cart_items = Cart.objects.filter(user=emailid)
        street_address = request.POST.get('StreetAddress', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        country = request.POST.get('Country', '')
        pincode = request.POST.get('pincode', '0')

        # Create Order
        order = Order.objects.create(user=cust,StreetAddress=street_address,City=city,State=state,Country=country,PinCode=pincode,TotalBill=tprice)

        # Move Cart Items to Order Items
        for item in cart_items:
            if item.helmet:
                product = item.helmet
            elif item.jacket:
                product = item.jacket
            elif item.gloves:
                product = item.gloves
            elif item.boots:
                product = item.boots
            elif item.kneeguard:
                product = item.kneeguard
            elif item.riding_pants:
                product = item.riding_pants
            else:
                continue  # Skip if no product found

            OrderItem.objects.create(order=order,product_name=product.name,product_price=product.price,product_image=product.image,quantity=item.quantity,
                size=product.size if hasattr(product, "size") else None,
                color=product.color if hasattr(product, "color") else None,
            )

        # Generate unique order number
        order_no = date.today().strftime("%Y%m%d") + str(order.id)
        order.orderNo = order_no
        order.save()

        razorpay_client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        currency = 'INR'
        amount = 2000  #razorpay take paisa
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        return render(request, 'confirmorder.html', {'orderobj': order, 'context': context, 'cart_items': cart_items})
    else:
        cart_items = Cart.objects.filter(user=cust)
        tprice=tprice
        return render(request,'checkout.html',{'tprice':tprice,'cust':cust,'cart_items': cart_items})

def paymentsuccess(request,totalprice):
    oid = request.GET.get('order_id', '')
    pid = request.GET.get('payment_id', '')
    tbill = totalprice
    useremail=request.session['user_emailId']
    user = UserModel.objects.filter(EmailId=useremail).first()

    # Fetch cart items of the user
    cart_items = Cart.objects.filter(user=useremail)
    total_items = cart_items.count()

    payment = Payment.objects.create(
        user=user,
        order_id=oid,
        payment_id=pid,
        total_bill=tbill,
        status="Completed"
    )

    if payment:
        # **Send email confirmation**
        subject = 'Your Order Has Been Placed'
        email_context = {
        'oid': oid,
        'pid': pid,
        'tbill': tbill,
        'user': user, 
        'cart_items': cart_items, 
        'total_items': total_items
    }
    
    html_content = render_to_string('orderplaced.html', email_context)  # Render HTML email
    text_content = strip_tags(html_content)  # Fallback text email content

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [request.session['user_emailId']]
    
    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")  # Attach HTML content
    email.send()


    return render(request, 'orderplaced.html', {'oid': oid, 'pid': pid, 'tbill': tbill, 'user': user, 'cart_items': cart_items, 'total_items': total_items})

# cart delete
def cartdelete(request):
    direct=reverse('home')
    flag='Mail Send'
    email = request.session['user_emailId']
    cartid=Cart.objects.filter(user=email)
    cartid.delete()
    return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}})

# usermanage View
def usermanage(request):
    user=UserModel.objects.all()
    admin=AdminModel.objects.all()
    return render(request,'usermanage.html',{'user':user,'admin':admin})

# dashboard View
def dashboard(request):
    heltotal=Helmet.objects.count()
    jactotal=Jacket.objects.count()
    glovtotal=Gloves.objects.count()
    boottotal=Boots.objects.count()
    Kneetotal=Kneeguard.objects.count()
    panttotal=RidingPants.objects.count()
    total_products = heltotal+jactotal+glovtotal+boottotal+Kneetotal+panttotal
    total_users = UserModel.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('TotalBill'))['total'] or 0  # Ensure field name matches
    # avg_rating = Review.objects.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0
    return render(request,'admin.html',{'totalproduct':total_products,'totaluser':total_users, 'totalorder':total_orders, 'totalrevenue':total_revenue,})


# adminsetting View
def adminsetting(request):
    if request.method=='POST':
        pass
    else:
        adminmail=request.session['adminemail']
        admindata=AdminModel.objects.get(adminEmailId=adminmail)
        return render(request,'adminsetting.html',{'admindata':admindata})

# adminsetting View
def ordersadmin(request):
    orders_data = Order.objects.prefetch_related('order_items').all()
    return render(request,'ordersadmin.html',{'orderdata':orders_data})

# FAQ View
def Faq(request):
    if request.method=='POST':
        direct=reverse('faq')
        flag='Question submited'
        email = request.session['user_emailId']
        ques = request.POST.get('ques')
        user=UserModel.objects.get(EmailId=email)
        data=FAQModel.objects.create(emailId=user,question=ques)
        data.save()
        return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}})
    else:
        return render(request,'FAQ.html')


# Add User
def RegiUser(request):
    if request.method=='POST':
        flag='Account Created'
        direct=reverse('login')
        fname=request.POST['fname']
        lname=request.POST['lname']
        emailid=request.POST['emailid']
        phno=request.POST['phno']
        password=request.POST['password']
        epass=make_password(password)
        dob=request.POST['dob']
        gender=request.POST['gender']
        StreetAddress=request.POST['StreetAddress']
        City=request.POST['City']
        State=request.POST['State']
        Country=request.POST['Country']
        PinCode=request.POST['PinCode']
        data=UserModel.objects.create(FirstName=fname,LastName=lname,EmailId=emailid,PhoneNo=phno,Password=epass,DOB=dob,Gender=gender,StreetAddress=StreetAddress,City=City,State=State,Country=Country,PinCode=PinCode)
        data.save()
        return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}})
    else:
        return render(request,'RegiUser.html')
    


# Login User/Admin
def login(request):
    passinc = 0 
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = UserModel.objects.filter(EmailId=email).first()
        admin = AdminModel.objects.filter(adminEmailId=email).first()
        if user:
            flag = check_password(password, user.Password)
            if flag:
                request.session['User_name'] = user.FirstName
                request.session['user_emailId'] = email
                return redirect('home')  
            else:
                passinc += 1  
                error_message = 'Incorrect password for user.'
        elif admin:
            if admin.adminPassword == password: 
                request.session['admin_name'] = admin.adminName
                request.session['adminemail']=email
                return redirect('admindashboard')
            else:
                passinc += 1  
                error_message = 'Incorrect password for admin.'
        else:
            error_message = 'User not found.'
        return render(request, 'login.html', {'error': error_message, 'passinc': passinc})
    return render(request, 'login.html', {'passinc': passinc})

# Forget Password
def forgpass(request):
    return render(request,'forpass.html')

# View Profile
def viewprof(request):
    email = request.session['user_emailId']
    user_m = UserModel.objects.get(EmailId=email)
    recent_orders = Order.objects.filter(user=user_m).prefetch_related(
        Prefetch('order_items')
    ).order_by('-created_at')[:3]
    return render(request, 'viewprofile.html', {'data': user_m, 'orders': recent_orders})

# edit profile
def Editprof(request):
    if request.method=='POST':
        flag='Profile Update'
        direct=reverse('home')
        fname=request.POST['fname']
        lname=request.POST['lname']
        emailid=request.POST['emailid']
        phno=request.POST['phno']
        password=request.POST['password']
        epass=make_password(password)
        dob=request.POST['dob']
        gender=request.POST['gender']
        StreetAddress=request.POST['StreetAddress']
        City=request.POST['City']
        State=request.POST['State']
        Country=request.POST['Country']
        PinCode=request.POST['PinCode']
        old_data=UserModel.objects.update(FirstName=fname,LastName=lname,EmailId=emailid,PhoneNo=phno,Password=epass,DOB=dob,Gender=gender,StreetAddress=StreetAddress,City=City,State=State,Country=Country,PinCode=PinCode)
        return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}})
    else:
        email=request.session['user_emailId']
        old_data=UserModel.objects.get(EmailId=email)
        return render(request,'Editprof.html',{'data':old_data})

def deleteuser(request,EmailId):
    flag='Profile deleted'
    direct=reverse('home')
    old_data=UserModel.objects.get(EmailId=EmailId)
    old_data.delete()
    return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}})

# LogOut User/Admin
def logout(request):
    flag='Log Out'
    direct=reverse('home')
    session_key=list(request.session.keys())
    for key in session_key:
        del request.session[key]
    return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}})


# Add Products
def Addproduct(request):
    passinc = 0
    direct=reverse('addproduct')
    if request.method=='POST':
        product_type = request.POST.get("product_type")
        name = request.POST.get("name")
        brand = request.POST.get("brand")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        image = request.FILES.get("image")
        
        if product_type == "helmet":
            flag='Helmet Added'
            helmet_type=request.POST.get("helmet_type")
            helmet_certifications=request.POST.get("helmet_certifications")
            helmet_size=request.POST.get("helmet_size")
            helmet_color=request.POST.get("helmet_color")
            product = Helmet.objects.create(name=name,brand=brand,price=price,stock_availability=stock,image=image,helmet_type=helmet_type,certifications=helmet_certifications,size=helmet_size,color=helmet_color)
            product.save()
            return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}})
        
        elif product_type == "jacket":
            flag='Jacket Added'
            jacket_type=request.POST.get("jacket_type")
            jacket_size=request.POST.get("jacket_size")
            jacket_color=request.POST.get("jacket_color")
            jacket_material=request.POST.get("jacket_material")
            jacket_certifications=request.POST.get("jacket_certifications")
            jacket_reflective=request.POST.get("jacket_Reflective")
            jacket_ventilation=request.POST.get("jacket_ventilation")
            jacket_padding=request.POST.get("jacket_padding")
            jacket_waterproofing=request.POST.get("jacket_waterproofing")
            product=Jacket.objects.create(name=name,brand=brand,price=price,stock_availability=stock,image=image,jacket_type=jacket_type,size=jacket_size,color=jacket_color,material=jacket_material,certifications=jacket_certifications,reflective_elements=jacket_reflective,ventilation_system=jacket_ventilation,padding_protection=jacket_padding,waterproofing=jacket_waterproofing)
            product.save()
            return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}})
        
        elif product_type == "gloves":
            flag='Gloves Added'
            gloves_type=request.POST.get("gloves_type")
            gloves_size=request.POST.get("gloves_size")
            gloves_color=request.POST.get("gloves_color")
            gloves_material=request.POST.get("gloves_material")
            gloves_certifications=request.POST.get("gloves_certifications")
            gloves_waterproofing=request.POST.get("gloves_waterproofing")
            gloves_touchscreen=request.POST.get("gloves_touchscreen")
            product=Gloves.objects.create(name=name,brand=brand,price=price,stock_availability=stock,image=image,gloves_type =gloves_type,size=gloves_size,color=gloves_color,material=gloves_material,certifications=gloves_certifications,waterproofing=gloves_waterproofing,touchscreen_compatibility=gloves_touchscreen)
            return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}})
        
        elif product_type == "boots":
            flag='Boots Added'
            boots_type=request.POST.get("boots_type")
            boots_size=request.POST.get("boots_size")
            boots_color=request.POST.get("boots_color")
            boots_material=request.POST.get("boots_material")
            boots_certifications=request.POST.get("boots_certifications")
            boots_closure=request.POST.get("boots_closure")
            boots_waterproofing=request.POST.get("boots_waterproofing")
            product=Boots.objects.create(name=name,brand=brand,price=price,stock_availability=stock,image=image,boots_type=boots_type,size=boots_size,color=boots_color,material=boots_material,certifications=boots_certifications,closure_type=boots_closure,waterproofing=boots_waterproofing)
            return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}})
        
        elif product_type == "Kneeguard":
            flag='Kneeguard Added'
            kneeguard_protection=request.POST.get("kneeguard_protection")
            kneeguard_straps=request.POST.get("kneeguard_straps")
            kneeguard_material=request.POST.get("kneeguard_material")
            product=Kneeguard.objects.create(name=name,brand=brand,price=price,stock_availability=stock,image=image,protection_level=kneeguard_protection,    adjustable_straps=kneeguard_straps,material=kneeguard_material)
            return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}})
        
        elif product_type == "riding_pants":
            flag='Riding Pants Added'
            pants_type=request.POST.get("pants_type")
            pants_size=request.POST.get("pants_size")
            pants_color=request.POST.get("pants_color")
            pants_material=request.POST.get("pants_material")
            pants_certifications=request.POST.get("pants_certifications")
            pants_Reflective=request.POST.get("pants_Reflective")
            pants_ventilation=request.POST.get("pants_ventilation")
            pants_padding=request.POST.get("pants_padding")
            pants_waterproofing=request.POST.get("pants_waterproofing")
            product=RidingPants.objects.create(name=name,brand=brand,price=price,stock_availability=stock,image=image,pants_type=pants_type,size=pants_size,color=pants_color,material=pants_material,certifications=pants_certifications,reflective_elements=pants_Reflective,ventilation_system=pants_ventilation,padding_protection=pants_padding,waterproofing=pants_waterproofing)
            return render(request, 'success.html', {'data': {'flag': flag , 'direct':direct}})
        
        else:
            passinc += 1 
            return render(request, 'AddProduct.html', {'passinc': passinc})
            
    else:
        return render(request,'AddProduct.html')
