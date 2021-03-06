from django import forms

class HeaderSearchForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2', 'placeholder': 'chercher'})
        )

class HomeSearchForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Produit'})
        )

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Identifiant',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    mail = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
        )
    password = forms.CharField(
        label='Mot de Passe',
        max_length=20,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        )
    password_check = forms.CharField(
        label='Confirmez votre Mot de Passe',
        max_length=20,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        )
    
class ConnexionForm(forms.Form):
    username = forms.CharField(
        label='Identifiant',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    password = forms.CharField(
        label='Mot de passe',
        max_length=20,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        )