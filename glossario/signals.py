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
    responsaveis = instance.responsavel.all()
    membros = instance.membros.all()
    responsaveis_group = Group.objects.get_or_create(name='responsaveis')[0]
    membros_group = Group.objects.get_or_create(name='membros')[0]

    for user in responsaveis:
        responsaveis_group.user_set.add(user)

    for user in membros:
        membros_group.user_set.add(user)

@receiver(post_save, sender=Sinal)
def update_upload_path(sender, instance, created, **kwargs):
    # o arquivo será salvo em MEDIA_ROOT/sinal_videos/convertidos/<id>-<tag>-<YYYY>-<MM>-<DD>-<HH><MM><SS>

    originais = '{0}/sinal_videos/originais'.format(settings.MEDIA_ROOT)
    convertidos = '{0}/sinal_videos/convertidos'.format(settings.MEDIA_ROOT)


    videoFields = [instance.sinalLibras, instance.descLibras, instance.exemploLibras, instance.varicLibras]
    tags = ['sinal', 'descricao', 'exemplo', 'variacao']

    for index, field in enumerate(videoFields):
        if field and instance.original_mode != field.name: # existe e foi alterado...
            original_file = field.name
            file_name_new = str(instance.id)+'-'+tags[index]+'-'+datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".mp4"
            new_file = convertidos+'/'+file_name_new
            subprocess.call('ffmpeg -i {0}/{1} -c:v libx264 -crf 19 -movflags faststart -threads 0 -preset slow -c:a aac -strict -2 {2}'
                .format(
                    originais,
                    str(field).split('/')[2],
                    new_file
                    ),
                    shell=True
                    )
            print("############## RAMON ####################")
            print(field.__dict__)
            print(field.field.name)
            name_update = 'sinal_videos/convertidos/'+file_name_new
            Sinal.objects.filter(id=instance.id).update(**{"%s" % field.field.name: name_update} )
