from django.contrib import admin
from .models import Product, ProductImage, ProductVideo, Color, Inquiry, ContactMessage, Flavour, Category, Testimonial, BlogPost

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductVideoInline]
    list_display = ('name', 'category', 'available_quantity', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category',)
    filter_horizontal = ('available_colors', 'available_flavours',)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer_name', 'submitted_at')
    readonly_fields = ('product', 'customer_name', 'customer_email', 'customer_phone', 'message')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at') 
    search_fields = ('full_name', 'email', 'subject')             
    readonly_fields = ('full_name', 'email', 'subject', 'message', 'created_at')
    list_filter = ('created_at',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'designation', 'is_active')
    list_filter = ('rating', 'is_active')
    search_fields = ('customer_name', 'review_text')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)} # Auto-fill slug from title
    search_fields = ('title', 'content')

admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Flavour)

