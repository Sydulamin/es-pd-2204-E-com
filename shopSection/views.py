from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from sslcommerz_lib import SSLCOMMERZ
# from sslcommerz_lib import SSLCOMMERZException


def product(request, id):
    product = Product.objects.get(id=id)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)[:3]
        cart_count = Cart.objects.filter(user=request.user).count()
    context = {
        'product': product,
        'cart_count': cart_count,
        'cart_items': cart_items
    }
    return render(request, "product_view.html", context)

def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    current_user = request.user
    Cart.objects.create(user=current_user, product=product)
    return redirect('Home')

def cart(request):
    cart_item = Cart.objects.filter(user=request.user)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)[:3]
        cart_count = Cart.objects.filter(user=request.user).count()
    context = {
        'cart_item': cart_item,
        'cart_items': cart_items,
        'cart_count': cart_count,
    }


    return render(request, "cart.html", context)

def plus_quantity(request):
    id = request.GET.get('cart_id')
    cart_obj = Cart.objects.get(id=id)
    if cart_obj.product.quantity > cart_obj.quantity:
        cart_obj.quantity += 1
        if cart_obj.product.discount_price != 0:
            cart_obj.cartPrice = cart_obj.quantity * cart_obj.product.discount_price
        else:
            cart_obj.cartPrice = cart_obj.quantity * cart_obj.product.price
        cart_obj.save()
        return JsonResponse({
            'status':200,
            'quantity':cart_obj.quantity,
            'price':cart_obj.cartPrice,
        })
    else:
        return JsonResponse({
            "status":401,
            'details':"This product has no more qunatities left",
            'quantity':cart_obj.quantity
        })

def minus_quantity(request):
    id = request.GET.get('cart_id')
    cart_obj = Cart.objects.get(id=id)
    if cart_obj.quantity > 1:
        cart_obj.quantity -= 1
        if cart_obj.product.discount_price != 0:
            cart_obj.cartPrice = cart_obj.quantity * cart_obj.product.discount_price
        else:
            cart_obj.cartPrice = cart_obj.quantity * cart_obj.product.price
        cart_obj.save()
        return JsonResponse({
            'status':200,
            'quantity':cart_obj.quantity,
            'price':cart_obj.cartPrice,
        })
    else:
        return JsonResponse({
            'status':401,
            "quantity":cart_obj.quantity,
            "price":cart_obj.cartPrice,
        })


def removeCart(request):
    id = request.GET.get('cart_id')
    cart_obj = Cart.objects.get(id=id)
    cart_obj.delete()
    return JsonResponse({
        "status":200,
        "details":"deleted successfully"
    })

def sslcommerz_success(request):
    return render(request, 'success.html')

def sslcommerz_fail(request):
    return render(request, 'fail.html')


def sslcommerz_payment(request):
    user = request.user

    cart_product = [p for p in Cart.objects.all() if p.user == user]
    # print(cart_product)
    amount = 0.00
    if cart_product:
        for p in cart_product:
            tempamount = p.cartPrice + 1
            amount += tempamount
    print(amount)

    sslcz = SSLCOMMERZ({'store_id': 'niyam6412dc52e1e89', 'store_pass': 'niyam6412dc52e1e89@ssl', 'issandbox': True})
    total_amount = request.GET.get('totalAmu')
    print(total_amount)
    data = {
        'total_amount': amount,
        'currency': "BDT",
        'tran_id': "tran_12345",
        'success_url': "http://127.0.0.1:8000/payment/success/",
        # if transaction is succesful, user will be redirected here
        'fail_url': "http://127.0.0.1:8000/payment/fail/",  # if transaction is failed, user will be redirected here
        # 'cancel_url': "http://127.0.0.1:8000/payment-cancelled",
        # after user cancels the transaction, will be redirected here
        'emi_option': "0",
        'cus_name': "test",
        'cus_email': "test@test.com",
        'cus_phone': "01700000000",
        'cus_add1': "customer address",
        'cus_city': "Dhaka",
        'cus_country': "Bangladesh",
        'shipping_method': "NO",
        'multi_card_name': "",
        'num_of_item': 1,
        'product_name': "Test",
        'product_category': "Test Category",
        'product_profile': "general",
    }

    response = sslcz.createSession(data)
    return redirect(response['GatewayPageURL'])
    # if request.method == 'POST':
    #     sslcommerz = SSLCOMMERZ({
    #         'store_id': 'niyam6412dc52e1e89',
    #         'store_pass': 'niyam6412dc52e1e89@ssl',
    #         'total_amount': amount,
    #         'currency': 'BDT',
    #         'tran_id': 'your_transaction_id',
    #         'success_url': 'http://localhost:8000/payment/success/',
    #         'fail_url': 'http://localhost:8000/payment/fail/',
    #         # 'cancel_url': 'http://localhost:8000/cancel/',
    #         # 'ipn_url': 'http://localhost:8000/ipn/',
    #     })
    #
    #     try:
    #         payment_request = sslcommerz.init_payment()
    #         # response = sslcommez.createSession(post_body)
    #         # return 'https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=' + response["sessionkey"]
    #     except Exception as e:
    #         return render(request, 'error.html', {'error': str(e)})
    # else:
    #     return render(request, 'payment_form.html')

