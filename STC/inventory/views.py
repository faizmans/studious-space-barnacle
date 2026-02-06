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

from django.core.paginator import Paginator # <--- Import this at the top
from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request, category_id=None):
    # 1. Start with ALL products (Ordered)
    products_list = Product.objects.all().order_by('-created_at')
    
    # 2. Setup Categories
    categories = Category.objects.all()
    category = None

    # 3. Apply Category Filter
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products_list = products_list.filter(category=category)

    # 4. Apply Search Filter
    search_query = request.GET.get('q')
    if search_query:
        products_list = products_list.filter(name__icontains=search_query)

    # --- 5. PAGINATION LOGIC (NEW) ---
    # Show 12 products per page (Change 12 to whatever number you prefer)
    paginator = Paginator(products_list, 12) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj, # Pass the page object, not the full list
        'categories': categories,
        'current_category': category,
        'search_query': search_query
    }
    return render(request, 'inventory/product_list.html', context)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Inquiry  
from .forms import InquiryForm

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

    # 3. Convert QuerySets to Lists
    images = list(product.images.all())
    videos = list(product.videos.all())
    
    # 4. Fetch Colors
    colors = product.available_colors.all()

    # --- 5. NEW: Fetch Related Products ---
    # Logic: Same category, exclude current product, take first 4
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk).order_by('-created_at')[:4]

    context = {
        'product': product,
        'form': form,
        'images': images,
        'videos': videos,
        'colors': colors,
        'related_products': related_products, # Add to context
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



from django.views.decorators.http import require_POST
from .cart import Cart # Import the class we just made

# --- 1. ADD TO QUOTE ---
@require_POST
def add_to_quote(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # Get quantity from form, default to 1
    quantity = request.POST.get('quantity', 1) 
    cart.add(product=product, quantity=quantity)
    messages.success(request, f"{product.name} added to your Inquiry List.")
    return redirect('product_detail', pk=product_id)

# --- 2. REMOVE FROM QUOTE ---
def remove_from_quote(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, "Item removed from list.")
    return redirect('quote_list')

# --- 3. VIEW QUOTE BASKET & SUBMIT ---
def quote_list(request):
    cart = Cart(request)
    
    # Handle the "Bulk Inquiry" Form
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            
            # 1. Build the list string
            product_list_str = "--- BULK INQUIRY BASKET ---\n"
            for item in cart:
                product_list_str += f"• {item['product'].name} | Qty: {item['quantity']}\n"
            product_list_str += "---------------------------\n"
            
            # 2. Add list to message
            inquiry.message = product_list_str + "\nUSER NOTE:\n" + (inquiry.message or "")
            
            # 3. Set product to None (It's a bulk order)
            inquiry.product = None # <--- NO SINGLE PRODUCT LINK
            
            inquiry.save()
            cart.clear()
            messages.success(request, "Bulk inquiry sent! We will quote you shortly.")
            return redirect('home')
    else:
        form = InquiryForm()

    return render(request, 'inventory/quote_list.html', {'cart': cart, 'form': form})


from .models import Product, Category, Testimonial 
def home(request):
    products = Product.objects.all()
    # Fetch active reviews
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at') 
    
    context = {
        'products': products,
        'testimonials': testimonials, # <--- Pass to template
    }
    return render(request, 'inventory/home.html', context)


from django.core.paginator import Paginator
from django.shortcuts import render
from .models import BlogPost

def blog_list(request):
    # 1. Fetch all posts (Database query is lazy, so this doesn't hit DB yet)
    all_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    
    # 2. Set up Pagination (9 posts per page)
    paginator = Paginator(all_posts, 9) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/blog_list.html', {'page_obj': page_obj})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    # SEO Context: Pass meta tags to the template
    return render(request, 'inventory/blog_detail.html', {'post': post})



def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # HERE: You can save this to a database model later if you want.
        # For now, we just print it to the console to confirm it works.
        print(f"--------------------------")
        print(f"NEW NEWSLETTER SUBSCRIBER: {email}")
        print(f"--------------------------")
        
        messages.success(request, "Success! The Price List has been sent to your email.")
        
    return redirect('home')