from django import forms
from django.db import transaction

from django.forms import ModelForm, TextInput, Textarea, Select, DateTimeInput, EmailField, CheckboxInput
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class AddCaseForm(forms.Form):
    class Meta:
        model = Case
        fields = '__all__'

REGIONS = [
    ('Нур-Султан', 'Нур-Султан'),
    ('Алматы', 'Алматы'),
    ('Шымкент','Шымкент'),
    ('Абаевская', 'Абаевская'),
    ('Акмолинская', 'Акмолинская'),
    ('Актюбинская', 'Актюбинская'),
    ('Алматинская', 'Алматинская'),
    ('Атырауская', 'Атырауская'),
    ('Восточно-Казахстанская', 'Восточно-Казахстанская'),
    ('Жамбылская', 'Жамбылская'),
    ('Жетысуская', 'Жетысуская'),
    ('Западно-Казахстанская', 'Западно-Казахстанская'),
    ('Карагандинская', 'Карагандинская'),
    ('Костанайская', 'Костанайская'),
    ('Кызылординская', 'Кызылординская'),
    ('Мангистауская', 'Мангистауская'),
    ('Павлодарская', 'Павлодарская'),
    ('Северо-Казахстанская', 'Северо-Казахстанская'),
    ('Улытауская','Улытауская'),
    ('Южно-Казахстанская', 'Южно-Казахстанская')
]
EDUCATION = [
    ('Высшее', 'Высшее'), ('ср-спе', 'Среднее-специальное'), ('среднее', 'Среднее'), ('Нет образования', 'Нет образования')
]
COURSE = [
        ('1', '1'),
        ('2', '2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('6','6'),
    ]
''''Форма студента'''
class StudentSignUpForm(UserCreationForm):
    Fio = forms.CharField(required=True, label='ФИО', widget=forms.TextInput(attrs={'class': 'form-control',
                                  'type': 'text',
                                  'required': 'true',
    }),)
    Educational_institution = forms.CharField(required=True,label='Учебное учрежедение')
    age = forms.CharField(required=True,label='Возраст')
    region = forms.ChoiceField(required=True,widget=forms.Select, choices=REGIONS,label='Область')
    Direction_of_study = forms.CharField(required=True,label='Специальность')
    Education = forms.ChoiceField(required=True,widget=forms.Select, choices= EDUCATION,label='Образование')

    Fio.widget.attrs.update({'class': 'form-control'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email','phone']
        field_classes = {'email': EmailField}



    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        user.save()
        student = Student.objects.create(user=user)
        student.Fio = self.cleaned_data.get('Fio')
        student.age = self.cleaned_data.get('age')
        student.region = self.cleaned_data.get('region')
        student.Educational_institution = self.cleaned_data.get('Educational_institution')
        # student.region = self.cleaned_data.get('Регион')
        # student.Course = self.cleaned_data.get('Курс')
        student.Direction_of_study = self.cleaned_data.get('Direction_of_study')
        student.Education = self.cleaned_data.get('Education')
        student.Course = self.cleaned_data.get('Course')
        student.save()
        return user

''''Форма Партнера'''
class PartnerSignUpForm(UserCreationForm):
    Fio = forms.CharField(required=True,label='ФИО')
    name_of_partner = forms.CharField(required=True,label='Название организации')
    site = forms.URLField(required=True,label='Сайт')

    class Meta(UserCreationForm.Meta):
        fields = ['email','phone']
        field_classes = {'email': EmailField}
        model = User



    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_partner = True
        user.is_staff = True
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        user.save()
        partner = Partner.objects.create(user=user)
        partner.Fio = self.cleaned_data.get('Fio')
        partner.name_of_partner = self.cleaned_data.get('name_of_partner')
        partner.site = self.cleaned_data.get('site')
        partner.save()
        return user

'''Форма создание кейса'''
class DateInput(forms.DateInput):
    input_type = 'date'
class AddCaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"
    class Meta:
        model = Case
        fields = ['title', 'description','file', 'category', 'region', 'date_of_close','tags']
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название кейса'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание кейса'
            }),
            "category": Select (attrs={
                'class': 'form-control',
                'placeholder': 'Выберите категорию'
            }),
            "region": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите регион'
            }),
            "date_of_close": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата завершения кейса'
            }),
            "tags": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Теги',
            }),
        }

'''Форма добавления ответа'''
class AddAnswer(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['Url', 'File', ]

'''Форма авторизации ответа'''
class LoginUserForm(AuthenticationForm):
    email = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

