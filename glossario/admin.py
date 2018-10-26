# -*- coding: utf-8 -*-
from glossario.forms import GlossarioForm, SinalForm, GrupoCMForm, CMForm, LocalizacaoForm
from unicodedata import normalize
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.db.models import Q
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# -----------------------------------------Criação de Usuario-------------------------------------------------------------------


from glossario.models import UserGlossario


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserGlossario
        fields = ('email', 'nome_completo')

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
        fields = ('email', 'password', 'nome_completo', 'is_active', 'is_superuser')

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
    list_display = ('email', 'nome_completo', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nome_completo',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome_completo', 'password1', 'password2')}
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



# ------------------------------------------------------------------------------------------------------------------------------

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

    def image_tag(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="50" height="50"/>'.format(obj.imagem.url))
            format_html('<img src="{}" width="50" height="50"/>')
        else:
            return format_html('<p>Sem imagem</p>')



class SinalAdmin(admin.ModelAdmin):

    form = SinalForm
    list_display = ('traducaoP', 'traducaoI', 'tema', 'glossario', 'image_tag_cmE', 'image_tag_cmD', 'image_tag_localizacao', 'publicado')
    list_filter = ('tema', 'glossario', 'localizacao', 'dataPost', 'publicado')
    actions = ['publicar_sinal',]

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

    def image_tag_cmE(self, obj):
        if obj.cmE.imagem:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.cmE.imagem.url))
        else:
            return format_html('<p>Sem Imagem</p>')
        image_tag_cmE.short_description = "Esquerda"

    def image_tag_cmD(self, obj):
        if obj.cmD.imagem:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.cmD.imagem.url))
        else:
            return format_html('<p>Sem Imagem</p>')
        image_tag_cmD.short_description = 'direita'

    def image_tag_localizacao(self, obj):
        if obj.localizacao.imagem:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.localizacao.imagem.url))
        else:
            return format_html('<p>Sem Imagem</p>')
        image_tag_localizacao.short_description = 'localização'

    def get_queryset(self, request):
        qs = super(SinalAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(glossario__responsavel=request.user) | Q(glossario__membros=request.user)).distinct()


class GrupoCMAdmin(admin.ModelAdmin):

    form = GrupoCMForm
    list_display = ('__str__', 'image_tag', 'bsw')

    def image_tag(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="50" height="50"/>'.format(obj.imagem.url))
        else:
            return format_html('<p>Sem imagem</p>')
    image_tag.short_description = 'Imagem'
    image_tag.allow_tags = True

class CMAdmin(admin.ModelAdmin):
    form = CMForm
    list_display = ('__str__', 'image_tag', 'bsw')

    def image_tag(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="50" height="50"/>'.format(obj.imagem.url))
        else:
            return format_html('<p>Sem Imagem</p>')
        image_tag.short_description = 'Imagem'
        image_tag.allow_tags = True

class LocalizacaoAdmin(admin.ModelAdmin):
    form = LocalizacaoForm
    list_display = ('nome', 'image_tag', 'bsw')

    def image_tag(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="50" height="50"/>'.format(obj.imagem.url))
        else:
            return format_html('<p>Sem imagem</p>')
        image_tag.short_description = 'Imagem'
        image_tag.allow_tags = True


admin.site.register(Tema)
admin.site.register(Glossario, GlossarioAdmin)
admin.site.register(Sinal, SinalAdmin)
admin.site.register(GrupoCM, GrupoCMAdmin)
admin.site.register(CM, CMAdmin)
admin.site.register(Localizacao, LocalizacaoAdmin)



