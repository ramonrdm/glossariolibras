from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from glossario.models import Glossario, Sinal
from django.conf import settings
import subprocess
import datetime
from django.core.files.base import ContentFile
import os, os.path
from django.core.files.base import File
from django.db.models import FileField


@receiver(post_save, sender=Glossario)
def set_new_user_group(sender, instance, **kwargs):
    responsaveis = instance.responsaveis.all()
    membros = instance.membros.all()
    responsaveis_group = Group.objects.get_or_create(name='responsaveis')[0]
    membros_group = Group.objects.get_or_create(name='membros')[0]

    for user in responsaveis:
        responsaveis_group.user_set.add(user)

    for user in membros:
        membros_group.user_set.add(user)

@receiver(post_save, sender=Sinal)
def update_upload_path(sender, instance, created, **kwargs):
    
    url_base = settings.MEDIA_ROOT
    pasta_sinal_videos = '{0}/sinal_videos'.format(url_base)
    videoFields = [instance.video_sinal, instance.video_descricao, instance.video_exemplo, instance.video_variacao]
    tags = ['sinal', 'descricao', 'exemplo', 'variacao']

    for index, field in enumerate(videoFields):
        if field and instance.videos_originais_converter[index] != field.name:
            nome_video_converter = str(instance.id)+'-'+tags[index]+'-'+datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".mp4"
            arquivo_video_converter = pasta_sinal_videos+'/'+nome_video_converter
            
            subprocess.call('ffmpeg -i {0}/{1} -y -hide_banner -nostats -c:v libx264 -crf 19 -movflags faststart -threads 0 -preset slow -an -strict -2 {2}'
                .format(
                    url_base,
                    field.name,
                    arquivo_video_converter
                    ),shell=True)
            print("############# VIDEO CONVERTER ###############")
            print(instance.videos_originais_converter[index])
            print(field.name)
            print(arquivo_video_converter)
            nome_relativo_arquivo_convertido = 'sinal_videos/'+nome_video_converter
            Sinal.objects.filter(id=instance.id).update(**{"%s" % field.field.name: nome_relativo_arquivo_convertido} )
            if os.path.isfile(url_base+'/'+field.name):
                print("deletando    " + url_base+'/'+field.name)
                os.remove(url_base+'/'+field.name)
            if os.path.isfile(url_base+'/'+str(instance.videos_originais_converter[index])):
                print("deletando    " +  url_base+'/'+str(instance.videos_originais_converter[index]))
                os.remove(url_base+'/'+str(instance.videos_originais_converter[index]))
            print("############ ############## #################")

        else:
            print("############## NÃO MUDOU ####################")
            print(instance.videos_originais_converter[index])
            print(field.name)
            if field.name == '' and instance.videos_originais_converter[index] != '':
                print("deletando    " +  url_base+'/'+str(instance.videos_originais_converter[index]))
                os.remove(settings.MEDIA_ROOT+'/'+str(instance.videos_originais_converter[index]))
            print("############ ############## #################")

