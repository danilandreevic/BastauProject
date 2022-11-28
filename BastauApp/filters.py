import django_filters
from django_filters import DateFilter, CharFilter, FilterSet, ChoiceFilter
from django.forms import ModelForm, TextInput, Textarea, Select, DateTimeInput, EmailField, CheckboxInput
from .models import *

class CaseFilter(django_filters.FilterSet):
    search = CharFilter(field_name='title', lookup_expr='icontains', widget = TextInput(attrs={
            'class':'form-control', 'placeholder': 'Поиск...'
        }))
    tags = CharFilter(field_name='tags__name', lookup_expr='icontains', widget = TextInput(attrs={
            'class':'form-control', 'placeholder': 'Теги...'
        }))

    class Meta:
        model = Case
        fields = ['category','region', 'user_id']

