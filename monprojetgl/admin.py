from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Enseignant, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil'

class EnseignantAdmin(UserAdmin):
    inlines = (ProfileInline,)
    
    # Configuration obligatoire
    list_display = ('email', 'nom', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'nom')
    ordering = ('email',)  # Tri par email au lieu de username
    
    # Configuration des champs pour le formulaire d'édition
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('nom',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Configuration des champs pour le formulaire de création
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'password1', 'password2'),
        }),
    )

admin.site.register(Enseignant, EnseignantAdmin)


