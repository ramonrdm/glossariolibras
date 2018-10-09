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
from django.utils.html import format_html

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_lattes', 'is_staff', 'image_tag')
    list_select_related = ('profile',)

    def get_lattes(self, instance):
        return instance.profile.lattes
    get_lattes.short_description = 'Lattes'

    def image_tag(self, instance):
        if instance.profile.foto:
            return u'<img src="%s" width="50" height="50"/>' % instance.profile.foto.url
        else:
            return 'Sem foto'
    image_tag.short_description = 'Foto'
    image_tag.allow_tags = True

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

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
        return format_html('<img src="{}" width="50" height="50"/>'.format(obj.imagem.url))
    image_tag.short_description = 'Imagem'


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
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.cmE.imagem.url))
    image_tag_cmE.short_description = "Esquerda"

    def image_tag_cmD(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.cmD.imagem.url))
    image_tag_cmD.short_description = 'direita'

    def image_tag_localizacao(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.localizacao.imagem.url))
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
        return format_html('<img src="{}" width="50" height="50"/>'.format(obj.imagem.url))
    image_tag.short_description = 'Imagem'
    image_tag.allow_tags = True

class CMAdmin(admin.ModelAdmin):
    form = CMForm
    list_display = ('__str__', 'image_tag', 'bsw')

    def image_tag(self, obj):
        return format_html('<img src="{}" width="50" height="50"/>'.format(obj.imagem.url))
    image_tag.short_description = 'Imagem'
    image_tag.allow_tags = True

class LocalizacaoAdmin(admin.ModelAdmin):
    form = LocalizacaoForm
    list_display = ('nome', 'image_tag', 'bsw')

    def image_tag(self, obj):
        return format_html('<img src="{}" width="50" height="50"/>'.format(obj.imagem.url))
    image_tag.short_description = 'Imagem'
    image_tag.allow_tags = True

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Tema)
admin.site.register(Glossario, GlossarioAdmin)
admin.site.register(Sinal, SinalAdmin)
admin.site.register(GrupoCM, GrupoCMAdmin)
admin.site.register(CM, CMAdmin)
admin.site.register(Localizacao, LocalizacaoAdmin)
