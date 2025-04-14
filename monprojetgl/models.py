from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
import os
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.db import models
from django.conf import settings


class Ressource(models.Model):
    # Lien avec l'enseignant
    enseignant = models.ForeignKey(
        'Enseignant',
        on_delete=models.CASCADE,
        related_name='ressources'
    )
    
    nom_cours = models.CharField(max_length=200)
    description = models.TextField()
    date_cours = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    fichier_cours = models.FileField(upload_to='cours_fichiers/')

    def __str__(self):
        return self.nom_cours


class Cours(models.Model):
    matiere = models.CharField(max_length=100)
    salle = models.CharField(max_length=50)
    jour = models.CharField(max_length=20)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    enseignant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cours')

    def __str__(self):
        return f"{self.matiere} - {self.jour}"

class Associer(models.Model):
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ressource.nom_doc} associé à {self.cours.nom}"

class Resultat(models.Model):
    type = models.CharField(max_length=100)
    note = models.FloatField()
    date_resultat = models.DateField()
    cours = models.OneToOneField(Cours, on_delete=models.CASCADE)

    def __str__(self):
        return f"Résultat de {self.cours.nom}"

class Evenement(models.Model):
    # Lien avec l'enseignant
    enseignant = models.ForeignKey(
        'Enseignant',
        on_delete=models.CASCADE,
        related_name='evenements'
    )
    
    titre = models.CharField(max_length=100)
    description = models.TextField()
    heure = models.TimeField()

    def __str__(self):
        return self.titre

    
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from django.contrib.auth.hashers import make_password

def profile_picture_path(instance, filename):
    return f'profile_pics/user_{instance.user.id}/{filename}'

class EnseignantManager(BaseUserManager):
    def create_user(self, email, nom, password=None, **extra_fields):
        if not email:
            raise ValueError(_('L\'email doit être renseigné'))
        if not nom:
            raise ValueError(_('Le nom doit être renseigné'))
            
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nom=nom,
            **extra_fields
        )
        user.set_password(password)  # Cryptage automatique
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        
        return self.create_user(email, nom, password, **extra_fields)

def upload_to(instance, filename):
    # Génère un chemin unique pour chaque image
    ext = os.path.splitext(filename)[1]  # Récupère l'extension du fichier
    return f'enseignants/{instance.email}{ext}'  # Utilise l'email comme nom de fichier
 

class Enseignant(AbstractBaseUser, PermissionsMixin):
    # Informations de base
    email = models.EmailField(_('adresse email'), unique=True)
    nom = models.CharField(_('nom complet'), max_length=100)
    
    # Champ pour afficher le hash du mot de passe (lecture seule)
    mot_de_passe_hash = models.CharField(
        _('hash du mot de passe'),
        max_length=128,
        editable=False,
        blank=True
    )

    # Informations supplémentaires
    adresse = models.CharField(_('adresse'), max_length=255, blank=True, null=True)
    telephone = models.CharField(_('téléphone'), max_length=20, blank=True, null=True)
    fonction = models.CharField(_('fonction'), max_length=100, blank=True, null=True)
    
    # Réseaux sociaux
    twitter = models.URLField(_('Twitter'), blank=True, null=True)
    facebook = models.URLField(_('Facebook'), blank=True, null=True)
    instagram = models.URLField(_('Instagram'), blank=True, null=True)
    linkedin = models.URLField(_('LinkedIn'), blank=True, null=True)
    
    photo = models.ImageField(
        _('photo de profil'),
        upload_to='profile_pics/',
        default='profile_pics/default.jpg',
        null=True,
        blank=True,
        help_text=_('Uploader une image (JPG, PNG, GIF, etc.)'),
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'],
                message=_('Seules les images sont autorisées (JPG, PNG, GIF, etc.)')
            )
        ]
    )
    
    
    # Bio
    bio = models.TextField(_('biographie'), blank=True, null=True)

    # Permissions
    is_active = models.BooleanField(_('actif'), default=True)
    is_staff = models.BooleanField(_('équipe technique'), default=False)
    is_admin = models.BooleanField(_('administrateur'), default=False)

    # Dates
    date_joined = models.DateTimeField(_('date d\'inscription'), auto_now_add=True)
    last_login = models.DateTimeField(_('dernière connexion'), auto_now=True)

    objects = EnseignantManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom']

    class Meta:
        verbose_name = _('enseignant')
        verbose_name_plural = _('enseignants')
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.email})"

    def save(self, *args, **kwargs):
        # Si le mot de passe a changé, mettre à jour mot_de_passe_hash avec le mot de passe haché
        if self.password != self.mot_de_passe_hash:
            self.mot_de_passe_hash = make_password(self.password)
        super().save(*args, **kwargs)




    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Profile(models.Model):
    user = models.OneToOneField(
        Enseignant,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('utilisateur')
    )
    phone = models.CharField(_('téléphone'), max_length=20, blank=True, null=True)
    address = models.TextField(_('adresse'), blank=True, null=True)
    about = models.TextField(_('à propos'), blank=True, null=True)
    profile_picture = models.ImageField(
        _('photo de profil'),
        upload_to=profile_picture_path,
        default='profile_pics/default.jpg'
    )
    job_title = models.CharField(_('poste'), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _('profil')
        verbose_name_plural = _('profils')

    def __str__(self):
        return f'Profil de {self.user.nom}'

    def save(self, *args, **kwargs):
        """Gestion des images de profil"""
        if self.pk:
            try:
                old = Profile.objects.get(pk=self.pk)
                if old.profile_picture != self.profile_picture and old.profile_picture.name != 'profile_pics/default.jpg':
                    old.profile_picture.delete(save=False)
            except Profile.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Suppression propre de l'image"""
        if self.profile_picture.name != 'profile_pics/default.jpg':
            self.profile_picture.delete(save=False)
        super().delete(*args, **kwargs)

class Planning(models.Model):
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    jour = models.CharField(max_length=100)
    salle = models.CharField(max_length=100)
    cours = models.OneToOneField(Cours, on_delete=models.CASCADE)

    def __str__(self):
        return f"Planning de {self.cours.nom}"

class Faq(models.Model):
    question = models.CharField(max_length=255)
    reponse = models.TextField()
    date_ajout = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.question

# models.py

# models.py

from django.db import models
from django.conf import settings
from django.utils import timezone

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  # Utilisation de auto_now_add

    def __str__(self):
        return f"Notification for {self.user}"






