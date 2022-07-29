# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2021-04-17 13:25:38
# @Last Modified by:   Your name
# @Last Modified time: 2021-11-21 09:27:05
from django.shortcuts import render, redirect
# to use class based views instead of direct functions
from django.views import View

# import databases tables
from django.shortcuts import render
from shop.models.products import Products
from shop.models.vendorCustomer import vendorCustomer
from shop.models.userCustomer import userCustomer
from shop.models.orders import Order
from django.views import View


class Checkout(View):
    def get(self, request):
        return render(request, 'checkout.html')
    def post(self, request):
        firstname = request.POST.get('first')
        lastname = request.POST.get('last')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        order_date = request.POST.get('order_date')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        customer = request.session.get('username')

        cart = request.session.get('cart')
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_id(ids)
        # products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products,city,state,order_date,firstname,lastname)

        for product in products:
            image = product.image
            order = Order(
                product=product,
                # send email to usercustomer table and
                # assign it to customer
                customer=userCustomer(email=customer),
                first_name= firstname,
                last_name=lastname,
                email=email,
                price=product.price,
                address=address,
                phone=phone,
                city=city,
                pincode=pincode,
                state=state,
                order_date=order_date)

            # to update the details in db
            print("product in ck:",product)
            product.available  = False
            product.save()

            order.placeOrder()



        print(products)
        request.session['cart'] = {}
        return redirect('Orders')

