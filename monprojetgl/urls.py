from django.urls import path
from . import views
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.connexion, name='connexion'),  # Affiche la page de connexion à la racine
    path('inscription/', views.inscription, name='inscription'),  # Page d'inscription
    path('index/', views.index, name='index'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('profile/', views.profile_view, name='profile'),
    
    path('notifications/', views.all_notifications, name='get_notifications'),
    path('all_notifications/', views.all_notifications, name='all_notifications'),

    # Ressources
    path('ressources/', views.ressources, name='ressources'),
    
    path('change-password/', views.change_password, name='change_password'),
    # Planning
    path('planning/', views.planning, name='planning'),
    
    path('liste_cours_enseignant', views.liste_cours_enseignant, name='liste_cours_enseignant'),
    path("enregistrer_ressource/", views.enregistrer_ressource, name="enregistrer_ressource"),  # Ajoute cette route
    path("ajouter_evenement/", views.ajouter_evenement, name="ajouter_evenement"),
    # Suivi (redirection externe)
    path('suivi/', views.suivi, name='suivi'),
    path('recherche/', views.global_search, name='global_search'),
    # Profil utilisateurs
    path('users-profile/', views.users_profile, name='users-profile'),

    # FAQ
    path('pages-faq/', views.pages_faq, name='pages-faq'),

    # Contact
    path('pages-contact/', views.pages_contact, name='pages-contact'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
