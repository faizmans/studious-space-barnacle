from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from .forms import InquiryForm

from .models import Product, Category # Import Category
from django.shortcuts import render, get_object_or_404, redirect
from .forms import InquiryForm

def home(request):
    # Fetch all categories to display in the slider/grid
    categories = Category.objects.all()
    
    # Fetch only the 8 newest products for the "Featured" section
    featured_products = Product.objects.all().order_by('-created_at')[:8]
    
    context = {
        'categories': categories,
        'products': featured_products
    }
    return render(request, 'inventory/home.html', context)


from django.db.models import Q # Import Q for advanced lookups

def product_list(request, category_id=None):
    # 1. Start with ALL products
    products = Product.objects.all().order_by('-created_at')
    
    # 2. Setup Categories for the filter bar
    categories = Category.objects.all()
    category = None

    # 3. Apply Category Filter (if selected)
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)

    # 4. Apply Search Filter (Live Search Logic)
    search_query = request.GET.get('q') # Get the 'q' parameter from URL
    if search_query:
        # Filter by name (case-insensitive)
        products = products.filter(name__icontains=search_query)

    context = {
        'products': products,
        'categories': categories,
        'current_category': category,
        'search_query': search_query # Pass back so we can keep text in input
    }
    return render(request, 'inventory/product_list.html', context)
def product_detail(request, pk):
    # 1. Fetch product (Standard)
    product = get_object_or_404(Product, pk=pk)
    
    # 2. Handle Inquiry Form Submission
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.product = product
            inquiry.save()
            messages.success(request, "Your inquiry has been sent! We will contact you shortly.")
            return redirect('product_detail', pk=pk)
    else:
        form = InquiryForm()

    # 3. LOGIC FIX: Convert QuerySets to Lists
    # This prevents errors when the template tries to count (len) or access indexes
    images = list(product.images.all())
    videos = list(product.videos.all())
    
    # 4. Fetch Colors
    colors = product.available_colors.all()

    context = {
        'product': product,
        'form': form,
        'images': images,  # Passing as list is safer for the Gallery JS
        'videos': videos,  # Passing as list is safer for the Gallery JS
        'colors': colors
    }
    return render(request, 'inventory/product_detail.html', context)

from .forms import InquiryForm, ContactForm # Import the new form

def about(request):
    return render(request, 'inventory/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save() # <--- THIS LINE SAVES DATA TO ADMIN
            messages.success(request, "Thank you! Your message has been sent. We will get back to you shortly.")
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'inventory/contact.html', {'form': form})




from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Inquiry, ContactMessage # Ensure these are imported

# Security Check: Only Superusers pass
def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    # FIX: Use 'submitted_at' for Inquiries
    inquiries = Inquiry.objects.all().order_by('-submitted_at')
    
    # ContactMessage likely still uses 'created_at' (from our previous step)
    contact_messages = ContactMessage.objects.all().order_by('-created_at')

    context = {
        'inquiries': inquiries,
        'contact_messages': contact_messages,
    }
    return render(request, 'inventory/custom_admin.html', context)

@login_required
@user_passes_test(is_superuser)
def delete_item(request, model_type, pk):
    # Helper to delete items easily
    if model_type == 'inquiry':
        item = get_object_or_404(Inquiry, pk=pk)
    elif model_type == 'message':
        item = get_object_or_404(ContactMessage, pk=pk)
    
    item.delete()
    messages.success(request, "Item deleted successfully.")
    return redirect('admin_dashboard')