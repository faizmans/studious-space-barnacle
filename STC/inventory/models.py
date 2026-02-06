from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, help_text="e.g., #FF0000", blank=True)

    def __str__(self):
        return self.name

class Flavour(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)    
    name = models.CharField(max_length=200)
    description = models.TextField()
    available_quantity = models.CharField(max_length=100, help_text="e.g., 500kg, 200 packets")
    available_colors = models.ManyToManyField('Color', blank=True) 
    available_flavours = models.ManyToManyField(Flavour, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')

class ProductVideo(models.Model):
    product = models.ForeignKey(Product, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='products/videos/')
    title = models.CharField(max_length=100, blank=True)

class Inquiry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    message = models.TextField(default="I would like to know the price of this item.")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        product_name = self.product.name if self.product else "Bulk Inquiry"
        return f"Inquiry from {self.customer_name} - {product_name}"

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.full_name} - {self.subject}"

class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    # e.g. "Bakery Owner, Surat" or "Purchasing Manager"
    designation = models.CharField(max_length=100, blank=True) 
    review_text = models.TextField()
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} ({self.rating} Stars)"

# inventory/models.py
from django.utils.text import slugify

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True) # URL friendly name (e.g. top-10-bakeries)
    
    # Content
    content = models.TextField() # Main article text
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    
    # SEO Fields (Crucial for Google)
    meta_title = models.CharField(max_length=70, blank=True, help_text="Title that appears on Google Search")
    meta_description = models.TextField(max_length=160, blank=True, help_text="Short description for Google results")
    
    # Status
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def read_time(self):
        # Calculate read time based on word count (avg 200 words/min)
        return max(1, len(self.content.split()) // 200)

    def __str__(self):
        return self.title