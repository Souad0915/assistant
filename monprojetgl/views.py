from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import ConnexionForm
from django.urls import reverse


# Vue pour la page d'accueil
def index(request):
    return render(request, 'index.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Notification

def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)  # Vérification

        if user is not None:
            login(request, user)  # Connexion de l'utilisateur
            # Ajouter une notification pour la connexion
            Notification.objects.create(
                user=user,
                message="Vous êtes connecté avec succès.",
                read=False,  # Utiliser 'read' ici au lieu de 'is_read'
                type="Connexion"
            )
            return redirect('index')  # Rediriger vers index.html
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    
    return render(request, 'connexion.html')



def inscription(request):
    return render(request, 'inscription.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Enseignant, Notification

def inscription(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('inscription')

        if Enseignant.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('inscription')

        try:
            enseignant = Enseignant.objects.create_user(email=email, nom=nom, password=password)
            login(request, enseignant)  # Connecter l'utilisateur après inscription
            # Ajouter une notification pour l'inscription
            Notification.objects.create(
                user=enseignant,
                message="Bienvenue, vous êtes inscrit avec succès.",
                read=False,  # Utiliser 'read' ici au lieu de 'is_read'
                type="Inscription"
            )
            messages.success(request, "Inscription réussie. Bienvenue !")
            return redirect('connexion')  # Redirection vers index.html
        except Exception as e:
            messages.error(request, f"Erreur lors de l'inscription: {str(e)}")
            return redirect('inscription')

    return render(request, 'inscription.html')


from django.shortcuts import render, redirect
from django.http import HttpResponse



# Vue pour la page des ressources
def ressources(request):
    return render(request, 'ressources.html')


# Vue pour la page de suivi (redirection externe)
def suivi(request):
    return redirect('http://localhost:8502')  # Redirige vers une URL externe

# Vue pour la page de profil utilisateur
def users_profile(request):
    return render(request, 'users-profile.html')

# Vue pour la page FAQ
def pages_faq(request):
    return render(request, 'pages-faq.html')

# Vue pour la page de contact
def pages_contact(request):
    return render(request, 'pages-contact.html')

from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Notification

def deconnexion(request):
    # Créer une notification pour la déconnexion
    if request.user.is_authenticated:
        Notification.objects.create(
            user=request.user,
            message="Vous avez été déconnecté avec succès.",
            read=False,
            type="Déconnexion"
        )
    logout(request)
    return redirect('connexion')  # Redirige vers la page de connexion


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm, ProfilePictureForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import os
from django.conf import settings
from .models import Notification  # Assurez-vous d'importer Notification

@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=request.user)
        picture_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        
        if 'update_profile' in request.POST:
            if profile_form.is_valid() and picture_form.is_valid():
                # Gestion de la suppression de l'ancienne image
                if 'photo' in request.FILES:
                    old_photo = request.user.photo
                    if old_photo and old_photo.name != 'profile_pics/default.jpg':
                        old_photo_path = os.path.join(settings.MEDIA_ROOT, old_photo.name)
                        if os.path.exists(old_photo_path):
                            os.remove(old_photo_path)
                
                profile_form.save()
                picture_form.save()
                # Ajouter une notification pour la mise à jour du profil
                Notification.objects.create(
                    user=request.user,
                    message="Votre profil a été mis à jour avec succès.",
                    read=False,  # Changement ici
                    type="Mise à jour du profil"
                )
                messages.success(request, 'Profil mis à jour avec succès!')
                return redirect('profile')
                
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                # Ajouter une notification pour le changement de mot de passe
                Notification.objects.create(
                    user=request.user,
                    message="Votre mot de passe a été changé avec succès.",
                    read=False,  # Changement ici
                    type="Changement de mot de passe"
                )
                messages.success(request, 'Mot de passe changé avec succès!')
                return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user)
        picture_form = ProfilePictureForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'users-profile.html', {
        'profile_form': profile_form,
        'picture_form': picture_form,
        'password_form': password_form,
    })

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from .models import Notification  # Assurez-vous d'importer votre modèle Notification

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from .models import Notification
import logging

logger = logging.getLogger(__name__)

@login_required
def change_password(request):
    if request.method == 'POST' and 'change_password' in request.POST:
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        errors = {}
        user = request.user

        # Vérifications
        if not user.check_password(old_password):
            errors['old_password'] = _("Votre ancien mot de passe est incorrect.")

        if new_password1 != new_password2:
            errors['new_password2'] = _("Les nouveaux mots de passe ne correspondent pas.")

        if len(new_password1) < 8:
            errors['new_password1'] = _("Le mot de passe doit contenir au moins 8 caractères.")

        if not errors:
            try:
                # Changement du mot de passe
                user.set_password(new_password1)
                user.save()
                
                # Mise à jour de la session CRUCIALE
                update_session_auth_hash(request, user)
                
                # Notification
                Notification.objects.create(
                    user=user,
                    message=_("Votre mot de passe a été changé avec succès."),
                    read=False,
                    type="password_change"
                )
                
                messages.success(request, _("Mot de passe changé avec succès. Vous êtes toujours connecté."))
                return redirect('users-profile')
                
            except Exception as e:
                logger.error(f"Password change failed: {str(e)}", exc_info=True)
                messages.error(request, _("Une erreur technique est survenue. Veuillez réessayer."))
        else:
            # Afficher les erreurs
            for field, error in errors.items():
                messages.error(request, error)

    return render(request, 'users-profile.html', {'active_tab': 'password'})


from django.shortcuts import render
from .models import Notification
from django.http import JsonResponse

def get_notifications(request):
    # Récupérer les notifications de l'utilisateur connecté qui ne sont pas lues
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    notifications_data = [
        {
            'message': notification.message,
            'created_at': notification.created_at.strftime("%H:%M %d/%m/%Y"),
            'id': notification.id
        }
        for notification in notifications
    ]
    return JsonResponse({'notifications': notifications_data})

# views.py

def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if notification.user == request.user:
        notification.read = True
        notification.save()
    return redirect('profile')

from django.contrib.auth.decorators import login_required

@login_required
def all_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cours

@login_required
def liste_cours_enseignant(request):
    utilisateur = request.user  # Utilisateur connecté
    print(f"Utilisateur connecté : {utilisateur}")  # Vérification de l'ID de l'utilisateur

    # Récupère les cours de l'enseignant
    cours_list = Cours.objects.filter(enseignant=utilisateur)

    # Affichage dans la console
    print(f"Cours récupérés : {cours_list}")

    # Redirection vers la vue planning avec les cours récupérés
    return redirect('planning')  # Redirige vers la vue de la page de planning

@login_required
def planning(request):
    utilisateur = request.user  # Utilisateur connecté
    cours_list = Cours.objects.filter(enseignant=utilisateur)

    # Affiche dans la console
    print(f"Cours récupérés dans planning : {cours_list}")

    # Retourne les cours au template
    return render(request, 'planning.html', {'cours_list': cours_list})

from django.shortcuts import render, redirect
from .models import Ressource
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def enregistrer_ressource(request):
    if request.method == 'POST':
        nom_cours = request.POST['nomCours']
        description = request.POST['descriptionCours']
        date_cours = request.POST['dateCours']
        heure_debut = request.POST['heureDebut']
        heure_fin = request.POST['heureFin']
        fichier = request.FILES.get('fichierCours')

        try:
            enseignant = request.user  # L'utilisateur connecté EST un enseignant

            ressource = Ressource(
                nom_cours=nom_cours,
                description=description,
                date_cours=date_cours,
                heure_debut=heure_debut,
                heure_fin=heure_fin,
                fichier_cours=fichier,
                enseignant=enseignant  # pas besoin de chercher, c'est déjà l'utilisateur connecté
            )
            ressource.save()

            messages.success(request, f"La ressource '{nom_cours}' a été enregistrée avec succès.")

        except Exception as e:
            messages.error(request, f"Erreur lors de l'enregistrement : {str(e)}")

    return render(request, 'ressources.html')


from django.shortcuts import render, redirect
from .models import Evenement
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def ajouter_evenement(request):
    if request.method == 'POST':
        titre = request.POST.get('titreEvenement')
        description = request.POST.get('descriptionEvenement')
        heure = request.POST.get('heure')

        try:
            enseignant = request.user  # L'utilisateur connecté est un Enseignant

            evenement = Evenement(
                titre=titre,
                description=description,
                heure=heure,
                enseignant=enseignant  # Lien avec l'utilisateur
            )
            evenement.save()
            messages.success(request, f"L'événement '{titre}' a été enregistré avec succès.")

        except Exception as e:
            messages.error(request, f"Erreur lors de l'enregistrement : {str(e)}")

    return render(request, 'ressources.html')

from django.shortcuts import render
from django.db.models import Q
from .models import Ressource, Evenement

def global_search(request):
    query = request.GET.get('query', '').strip().lower()

    results = []
    table_name = ""
    table = None
    enseignant = request.user  # L'enseignant connecté

    # Recherche dans les ressources pour l'enseignant connecté
    if query == 'ressources':
        results = Ressource.objects.filter(enseignant=enseignant)
        table_name = "Ressources"
        table = 'ressources'

    # Recherche dans les événements pour l'enseignant connecté
    elif query == 'evenements':
        results = Evenement.objects.filter(enseignant=enseignant)
        table_name = "Événements"
        table = 'evenements'

    # En cas de recherche vide, tu peux filtrer en fonction du nom de la ressource ou de l'événement
    elif query:
        # Recherche dans les ressources et événements en fonction de la requête
        results = Ressource.objects.filter(
            Q(nom_cours__icontains=query) | Q(description__icontains=query),
            enseignant=enseignant
        ) | Evenement.objects.filter(
            Q(titre__icontains=query) | Q(description__icontains=query),
            enseignant=enseignant
        )
        table_name = "Ressources et Événements"
        table = 'ressources_et_evenements'

    context = {
        'query': query,
        'table': table,
        'results': results,
        'table_name': table_name,
    }

    return render(request, 'search_results.html', context)
