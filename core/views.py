

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


# ============================================
# views.py
# ============================================
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import NewsletterSubscriber


def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@require_http_methods(["POST"])
def subscribe_newsletter(request):
    """Handle newsletter subscription."""
    try:
        email = request.POST.get('email', '').strip().lower()
        
        # Validate email presence
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Please enter your email address.'
            }, status=400)
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid email address.'
            }, status=400)
        
        # Check if already subscribed
        existing = NewsletterSubscriber.objects.filter(email=email).first()
        
        if existing:
            if existing.is_active:
                return JsonResponse({
                    'success': False,
                    'message': 'This email is already subscribed to our newsletter!'
                }, status=400)
            else:
                # Reactivate inactive subscriber
                existing.is_active = True
                existing.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Welcome back! Your subscription has been reactivated.'
                })
        
        # Create new subscriber
        ip_address = get_client_ip(request)
        NewsletterSubscriber.objects.create(
            email=email,
            ip_address=ip_address
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for subscribing! Check your inbox for exclusive updates.'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Oops! Something went wrong. Please try again later.'
        }, status=500)



def about(request):
    return render(request, "core/about.html", {})  

def service(request):
    return render(request, "core/service.html", {})

def contact_us(request):
    return render(request, "core/contact_us.html", {})


