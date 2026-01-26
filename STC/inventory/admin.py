from django.contrib import admin
from .models import Product, ProductImage, ProductVideo, Color, Inquiry, ContactMessage
from .models import Category

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductVideoInline]
    list_display = ('name', 'available_quantity')
    filter_horizontal = ('available_colors',)

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer_name', 'submitted_at')
    readonly_fields = ('product', 'customer_name', 'customer_email', 'customer_phone', 'message')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at') # Columns to show
    search_fields = ('full_name', 'email', 'subject')              # Search bar
    readonly_fields = ('full_name', 'email', 'subject', 'message', 'created_at') # Make read-only so you don't accidentally edit them
    list_filter = ('created_at',)

admin.site.register(Color)
admin.site.register(Category)

