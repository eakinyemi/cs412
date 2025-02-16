from django.shortcuts import render, redirect
import random
import datetime

# Create your views here.
MENU = {
    'Pizza': 12.99,
    'Burger': 8.99,
    'Pasta': 10.99,
    'Salad': 7.99,
}

DAILY = {
    'Sushi': 15.99,
    'Pesto Pasta': 12.99,
    'T-Bone Steak': 19.99,
    'Lobster': 24.99,
}

def main(request):
    return render(request, 'restaurant/main.html')

def order(request):
    daily_special = random.choice(list(DAILY.keys()))  
    context = {
        'menu': MENU,  
        'daily_special': daily_special,  
    }
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        special_requests = request.POST.get('special_requests')
        
        ordered_items = []
        total_price = 0

        for item in MENU.keys():
            if request.POST.get(item):  
                ordered_items.append(item)
                total_price += MENU[item]

        # Add Daily Special if selected
        daily_special = request.POST.get('daily_special')
        if daily_special and daily_special in DAILY:
            ordered_items.append(daily_special)
            total_price += DAILY[daily_special]

        ready_time = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(30, 60))

        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'special_requests': special_requests,
            'ordered_items': ordered_items,
            'total_price': round(total_price, 2),
            'ready_time': ready_time.strftime('%I:%M %p'),
        }
        return render(request, 'restaurant/confirmation.html', context)
    
    return redirect('restaurant:order')  
