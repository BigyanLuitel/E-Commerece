from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'brand', 'description', 'raw_notes', 'specs', 'price', 'stock', 'image', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'raw_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'specs': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': '{"RAM": "16GB", "Storage": "512GB"}'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'is_active':
                field.widget.attrs.setdefault('class', 'form-check-input')
            elif name not in ('description', 'raw_notes', 'specs'):
                field.widget.attrs.setdefault('class', 'form-control')