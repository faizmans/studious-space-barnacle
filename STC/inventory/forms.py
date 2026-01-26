from django import forms
from .models import Inquiry, ContactMessage

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['customer_name', 'customer_email', 'customer_phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ask for price or bulk details...'}),
            'customer_name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'customer_email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'customer_phone': forms.TextInput(attrs={'placeholder': 'Your Phone'}),
        }
# Add this class below your existing InquiryForm
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email Address', 'class': 'input-field'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'input-field'}),
            'message': forms.Textarea(attrs={'placeholder': 'How can we help you?', 'rows': 5, 'class': 'input-field'}),
        }