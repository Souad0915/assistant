# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    # Tu peux ajouter des champs personnalisés ici si nécessaire
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class ConnexionForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}), required=True)

# monprojetgl/forms.py

from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import Enseignant

class EnseignantProfileForm(UserChangeForm):
    password = None  # On ne veut pas afficher le champ password ici
    
    class Meta:
        model = Enseignant
        fields = ['nom', 'email', 'fonction', 'adresse', 'telephone', 
                 'bio', 'twitter', 'facebook', 'instagram', 'linkedin']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'nom': 'Nom Complet',
            'email': 'Adresse Email',
            'fonction': 'Fonction',
            'adresse': 'Adresse',
            'telephone': 'Téléphone',
            'bio': 'À Propos',
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = Enseignant
from django import forms
from .models import Enseignant, Profile
from django.contrib.auth.forms import PasswordChangeForm

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['nom', 'email', 'adresse', 'telephone', 'fonction',
                'twitter', 'facebook', 'instagram', 'linkedin', 'bio']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Enseignant
from django.core.exceptions import ValidationError

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['nom', 'email', 'fonction', 'adresse', 'telephone', 'bio',
                 'twitter', 'facebook', 'instagram', 'linkedin']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['photo']
        
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 2*1024*1024:  # 2MB
                raise ValidationError("L'image est trop grande (max 2MB)")
        return photo

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

from django import forms
from .models import Ressource
class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ['nom_cours', 'description', 'date_cours', 'heure_debut', 'heure_fin', 'fichier_cours']
