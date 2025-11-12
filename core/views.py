

from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from accounts.models import User
from django.core.paginator import Paginator
from core.models import *
from .forms import *

def home(request):
    users = User.objects.all()
    if not request.user.is_authenticated:
        return render(request, "core/index.html", {})
    else:
        user = request.user


        form = SearchCourierForm(request.GET)
        couriers = None

        if form.is_valid():
            tracking_id = form.cleaned_data['tracking_id']

            # Perform the search based on the tracking_id
            couriers = Courier.objects.filter(tracking_id=tracking_id)

        context = {
            "user": user,

            "couriers": couriers,
            "title": "Logistics"
        }

        return render(request, "core/transactions.html", context)



    
def logpage(request):
    return render(request, "core/logpage.html", {})  

from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import cache_control
from .models import Courier
from .forms import SearchCourierForm

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_courier(request):
    form = SearchCourierForm(request.GET)
    couriers = None
    context = {'form': form}

    if form.is_valid():
        tracking_id = form.cleaned_data['tracking_id']
        couriers = Courier.objects.filter(tracking_id=tracking_id)
        
        if couriers.exists():
            courier = couriers.first()
            
            # Build the complete URL and ensure HTTPS
            domain = request.get_host()
            if not request.is_secure():
                domain = f"https://{domain}"
            
            full_tracking_url = request.build_absolute_uri()
            if not full_tracking_url.startswith('https://'):
                full_tracking_url = full_tracking_url.replace('http://', 'https://')

            context.update({
                'courier': courier,
                'absolute_image_url': courier.package_image.url if courier.package_image else "",
                'tracking_url': full_tracking_url,
                'updated_time': timezone.now().isoformat(),
                'domain': domain
            })
    
    context['couriers'] = couriers
    return render(request, 'core/index.html', context)






def about(request):
    return render(request, "core/about.html", {})  

def service(request):
    return render(request, "core/service.html", {})

def contact_us(request):
    return render(request, "core/contact_us.html", {})


