# -*- coding: utf-8 -*-
from glossario.forms import GlossarioForm, SinalForm, GrupoCMForm, CMForm, LocalizacaoForm
from unicodedata import normalize
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from .models import *
from django.contrib.contenttypes.models import ContentType

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import UserGlossario


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserGlossario
        fields = ('email', 'date_of_birth')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserGlossario
        fields = ('email', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(UserGlossario, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


class GlossarioAdmin(admin.ModelAdmin):
    
    form = GlossarioForm
    list_display = ('nome', 'image_tag')
    list_filter = ('responsavel', 'membros', 'dataCriacao')
    
    def get_readonly_fields(self, request, obj=None):
        qs = super(GlossarioAdmin, self).get_queryset(request)
        qsResp = qs.filter(responsavel=request.user)
        qsMemb = qs.filter(membros=request.user)
        if obj in qsResp or request.user.is_superuser:
            return []
        if obj in qsMemb:
            return ('nome', 'responsavel', 'membros', 'imagem', 'videoGlossario', 'descricao')
        return []

    def get_actions(self, request):
        actions = super(GlossarioAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def get_queryset(self, request):
        qs = super(GlossarioAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(responsavel=request.user) | Q(membros=request.user)).distinct()

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def save_model(self, request, obj, form, change):
        gLink = obj.nome.lower()
        gLink = gLink.replace(" ", "-")
        gLink = normalize('NFKD', gLink)
        obj.link = gLink
        obj.save()  

class SinalAdmin(admin.ModelAdmin):

    form = SinalForm
    list_display = ('traducaoP', 'traducaoI', 'tema', 'glossario', 'image_tag_cmE', 'image_tag_cmD', 'image_tag_localizacao', 'publicado')
    list_filter = ('tema', 'glossario', 'localizacao', 'dataPost', 'publicado')
    actions = ['publicar_sinal',]

    def get_queryset(self, request):
        qs = super(SinalAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(glossario__responsavel=request.user) | Q(glossario__membros=request.user)).distinct()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "glossario":
            if request.user.is_superuser:
                kwargs["queryset"] = Glossario.objects.all()
            else:
                kwargs["queryset"] = Glossario.objects.filter(Q(responsavel=request.user) | Q(membros=request.user)).distinct()
        return super(SinalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.dataPost = datetime.date.today()
        obj.postador = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ['postador','dataPost']
        qs = super(SinalAdmin, self).get_queryset(request)
        qsResp = qs.filter(glossario__responsavel=request.user)
        # responsaveis = Glossario.objects.filter(responsavel=request.user)
        if not request.user.is_superuser:
            if obj not in qsResp:
                # self.exclude.append('publicado')
                self.exclude = ['postador','dataPost', 'publicado']
        return super(SinalAdmin, self).get_form(request, obj, **kwargs)

    def publicar_sinal(self, request, queryset):
        queryset.update(publicado=True)
    publicar_sinal.short_description = 'Publicar sinais selecionados'

class GrupoCMAdmin(admin.ModelAdmin):

    form = GrupoCMForm
    list_display = ('__str__', 'image_tag', 'bsw')

class CMAdmin(admin.ModelAdmin):

    form = CMForm
    list_display = ('__str__', 'image_tag', 'bsw')

class LocalizacaoAdmin(admin.ModelAdmin):

    form = LocalizacaoForm
    list_display = ('nome', 'image_tag', 'bsw')

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
admin.site.register(Tema)
admin.site.register(Glossario, GlossarioAdmin)
admin.site.register(Sinal, SinalAdmin)
admin.site.register(GrupoCM, GrupoCMAdmin)
admin.site.register(CM, CMAdmin)
admin.site.register(Localizacao, LocalizacaoAdmin)



