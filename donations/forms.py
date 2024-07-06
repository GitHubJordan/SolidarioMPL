# donations/forms.py

from django import forms
from .models import Donor, Donation, Item
from .models import News, Activity
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Nome de usuário"}),
        help_text="",
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Insira um nome de usuário válido. Exemplo de nome de usuário válido: jordan_adelino2",
            "unique": "Um usuário com esse nome já existe.",
        },
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
        help_text="",
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Digite um endereço de e-mail válido.",
            "unique": "Um usuário com este email já existe.",
        },
    )
    full_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Nome completo"}),
        help_text="",
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Insira um nome completo válido.",
        },
    )
    phone_number = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Telefone"}),
        help_text="",
        required=False,
        error_messages={
            "invalid": "Insira um número de telefone válido.",
        },
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Palavra-passe"}),
        help_text="",
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Digite uma senha válida.",
        },
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmar palavra-passe"}),
        help_text="",
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Insira uma confirmação de senha válida.",
        },
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "full_name", "phone_number", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""
        self.fields["email"].help_text = ""
        self.fields["full_name"].help_text = ""
        self.fields["phone_number"].help_text = ""

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn’t match.")
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError(
                "The password must be at least 8 characters long."
            )
        if password1.isdigit():
            raise forms.ValidationError("The password cannot be entirely numeric.")
        return password1


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "Nome de usuário"}),
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Insira um nome de usuário válido.",
        },
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Palavra-passe"}),
        error_messages={
            "required": "Este campo é obrigatório.",
            "invalid": "Digite uma senha válida.",
        },
    )


class DonorForm(forms.ModelForm):
    full_name = forms.CharField(
        label="Nome Completo",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nome Completo'}),
    )

    class Meta:
        model = Donor
        fields = ["full_name", "email", "phone", "profile_picture"]

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        if user_instance:
            self.fields['full_name'].initial = user_instance.full_name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Donor.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este email já está registrado.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and not phone.isdigit():
            raise forms.ValidationError("O telefone deve conter apenas números.")
        return phone


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ["amount", "message"]

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount <= 0:
            raise forms.ValidationError("O valor da doação deve ser maior que zero.")
        return amount


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price']  # Remova 'donated_by'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Nome do Item'
        self.fields['description'].label = 'Descrição'
        self.fields['price'].label = 'Preço'

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("O preço do item deve ser maior que zero.")
        return price

class ItemAdminForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'donated_by', 'estado']  # Inclua 'donated_by' e 'estado'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Nome do Item'
        self.fields['description'].label = 'Descrição'
        self.fields['price'].label = 'Preço'
        self.fields['donated_by'].label = 'Doador'
        self.fields['estado'].label = 'Estado do Item'

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise forms.ValidationError("O preço do item deve ser maior que zero.")
        return price

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'date']
        