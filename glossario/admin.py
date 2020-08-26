# -*- coding: utf-8 -*-
from glossario.forms import GlossarioForm, SinalForm, CMForm
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
from glossario.models import UserGlossario

class GlossarioAdmin(admin.ModelAdmin):
    
    form = GlossarioForm
    list_display = ('nome', 'image_tag')
    list_filter = ('responsaveis', 'membros', 'data_criacao')
    autocomplete_fields = ['responsaveis', 'membros']
    
    def get_readonly_fields(self, request, obj=None):
        qs = super(GlossarioAdmin, self).get_queryset(request)
        qsResp = qs.filter(responsaveis=request.user)
        qsMemb = qs.filter(membros=request.user)
        if obj in qsResp or request.user.is_superuser:
            return []
        if obj in qsMemb:
            return ('nome', 'responsaveis', 'membros', 'imagem', 'gad', 'descricao')
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
        return qs.filter(Q(responsaveis=request.user) | Q(membros=request.user)).distinct()

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def save_model(self, request, obj, form, change):
        gLink = obj.nome.lower()
        gLink = gLink.replace(" ", "-")
        gLink = normalize('NFKD', gLink).encode('ASCII', 'ignore').decode('ASCII')
        obj.link = gLink
        obj.save()  

    def image_tag(self, obj):
        if obj.imagem:
            return format_html('<img src="/media/{}" width="50" height="50"/>'.format(obj.imagem))
            format_html('<img src="{}" width="50" height="50"/>')
        else:
            return format_html('<p>Sem imagem</p>')

class SinalAdmin(admin.ModelAdmin):
    form = SinalForm
    readonly_fields=('data_criacao', 'postador')
    list_display = ('portugues', 'video_tag_sinal', 'ingles', 'glossario', 'image_tag_cmE', 'image_tag_cmD', 'image_tag_localizacao', 'image_tag_movimentacao' , 'publicado')
    list_filter = ('glossario', 'localizacao', 'movimentacao', 'publicado')
    actions = ['publicar_sinal',]
    search_fields = ('portugues', 'ingles')
    list_per_page = 30

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "glossario":
            if request.user.is_superuser:
                kwargs["queryset"] = Glossario.objects.all()
            else:
                kwargs["queryset"] = Glossario.objects.filter(Q(responsaveis=request.user) | Q(membros=request.user)).distinct()
        return super(SinalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.postador = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ['postador', 'create_data']
        if not request.user.is_superuser:
            if obj != None:
                responsaveis = obj.glossario.responsaveis.all()
                if not request.user in responsaveis:
                    self.exclude.append('publicado')
            else:
                self.exclude.append('publicado')

        return super(SinalAdmin, self).get_form(request, obj, **kwargs)

    def publicar_sinal(self, request, queryset):
        queryset.update(publicado=True)
    publicar_sinal.short_description = 'Publicar sinais selecionados'

    def video_tag_sinal(self, obj):
        if obj.video_sinal:
            return format_html('<video loop src="/media/{}" height="70" style="cursor:pointer;" onclick="this.paused?this.play():this.pause()" />'.format(obj.video_sinal))
        else:
            return format_html('<p>Sem Imagem</p>')

    def image_tag_cmE(self, obj):
        if obj.cmE:
            return format_html('<img style="border-radius: 25px 25px 25px 25px;" src="/static/img/configuracoes_de_mao/{}" width="50" height="50" />'.format(obj.cmE.imagem()))
        else:
            return format_html('<p>Sem Imagem</p>')
    image_tag_cmE.short_description = "Esquerda"

    def image_tag_cmD(self, obj):
        if obj.cmD:
            return format_html('<img style="border-radius: 25px 25px 25px 25px;" src="/static/img/configuracoes_de_mao/{}" width="50" height="50" />'.format(obj.cmD.imagem()))
        else:
            return format_html('<p>Sem Imagem</p>')
    image_tag_cmD.short_description = 'direita'

    def image_tag_localizacao(self, obj):
        if obj.localizacao:
            return format_html('<img src="/static/img/{}" width="50" height="50" />'.format(Localizacao.localizacoes_imagens[obj.localizacao]))
        else:
            return format_html('<p>Sem Imagem</p>')
    image_tag_localizacao.short_description = 'localização'

    def image_tag_movimentacao(self, obj):
        if obj.movimentacao:
            movimentacoes = dict(
                [('0', '0X.svg'), ('1', '1parede.png'), ('2', '2chao.png'), ('3', '3circular.png'), ('4', '4contato.png')])
            return format_html(
                '<img src="/static/img/{}" width="50" height="50" />'.format(movimentacoes[obj.movimentacao]))
        else:
            return format_html('<p>Sem Imagem</p>')
    image_tag_movimentacao.short_description = 'movimentacao'

    def get_queryset(self, request):
        qs = super(SinalAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(glossario__responsaveis=request.user) | Q(glossario__membros=request.user)).distinct()

class CMAdmin(admin.ModelAdmin):
    form = CMForm
    list_display = ('__str__', 'image_tag', 'bsw')
    readonly_fields = ["image_tag"]

    def image_tag(self, obj):
        if obj.imagem:
            return format_html('<img src="/static/img/configuracoes_de_mao/{}" width="50" height="50"/>'.format(obj.imagem()))
        else:
            return format_html('<p>Sem Imagem</p>')
    image_tag.short_description = 'Imagem'
    image_tag.allow_tags = True


class UserAdmin(BaseUserAdmin):
    search_fields = ('email','nome_completo')
    ordering = ('nome_completo',)
    filter_horizontal = ()
    list_display = ('nome_completo', 'email', 'is_superuser', 'last_login',)
    list_filter = ('is_superuser',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nome_completo',)}),
        ('Permissions', {'fields': ('is_superuser','is_active','is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome_completo', 'password1', 'password2')}
        ),
    )

admin.site.register(UserGlossario, UserAdmin)
admin.site.register(Glossario, GlossarioAdmin)
admin.site.register(Sinal, SinalAdmin)
admin.site.register(CM, CMAdmin)
