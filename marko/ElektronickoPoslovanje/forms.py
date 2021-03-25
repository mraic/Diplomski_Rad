from django.contrib.auth.forms import UserCreationForm
from . models import osobe
from django import forms
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = osobe
        fields = UserCreationForm.Meta.fields + ('email', 'broj_indeksa',)

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length = 255, help_text='Potrebna valjana e mail adresa.')

    class Meta:
        model = osobe
        fields = ('email', 'username', 'broj_indeksa', 'password1', 'password2')

    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = osobe.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email "{email}" je već u uporabi.')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = osobe.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f'Username "{username}" je već u uporabi.')

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = osobe
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")