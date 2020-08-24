import datetime
import logging
import subprocess
import os
import os.path
import math
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from glossario.models import Glossario, Sinal, UserGlossario


@receiver(post_save, sender=Glossario)
def set_news_group(sender, instance, **kwargs):
    responsaveis = instance.responsaveis.all()
    membros = instance.membros.all()
    responsaveis_group = Group.objects.get_or_create(name='responsaveis')[0]
    membros_group = Group.objects.get_or_create(name='membros')[0]

    for user in responsaveis:
        responsaveis_group.user_set.add(user)

    for user in membros:
        membros_group.user_set.add(user)


@receiver(post_save, sender=UserGlossario)
def set_new_user_group(sender, instance, **kwargs):
    user = UserGlossario.objects.get(id=instance.id)
    sugestoes, created = Glossario.objects.get_or_create(nome="Sugestões",)
    sugestoes.membros.add(user)
    membros_group = Group.objects.get_or_create(name='membros')[0]
    membros_group.user_set.add(user)


@receiver(post_save, sender=Sinal)
def update_upload_path(sender, instance, created, **kwargs):

    url_base = settings.MEDIA_ROOT
    pasta_sinal_videos = '{0}/sinal_videos'.format(url_base)
    pasta_sinal_preview = '{0}/sinal_preview'.format(url_base)
    video_fields = [instance.video_sinal, instance.video_descricao,
                   instance.video_exemplo, instance.video_variacao]
    preview_fields = [instance.preview1, instance.preview2,
                      instance.preview3, instance.preview4]
    tags = ['sinal', 'descricao', 'exemplo', 'variacao']

    for index, field in enumerate(video_fields):
        if field and instance.videos_originais_converter[index] != field.name:
            # Videos
            nome_video_converter = str(
                instance.id)+'-'+tags[index]+'-'+datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".mp4"
            arquivo_video_converter = pasta_sinal_videos+'/'+nome_video_converter

            subprocess.call('ffmpeg -i {0}/{1} -y -hide_banner -nostats -c:v libx264 -crf 19 -movflags faststart -threads 0 -preset slow -an -strict -2 {2}'
                            .format(
                                url_base,
                                field.name,
                                arquivo_video_converter
                            ), shell=True)
            nome_relativo_arquivo_convertido = 'sinal_videos/'+nome_video_converter
            Sinal.objects.filter(id=instance.id).update(
                **{"%s" % field.field.name: nome_relativo_arquivo_convertido})
            # Previews
            if not(index):
                # Pega o numero total de frames do video
                output = subprocess.run("ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 {0}".format(
                    arquivo_video_converter
                ), capture_output=True, shell=True, check=False)
                duration = output.stdout.decode()
                duration = math.ceil(int(duration)/4)

                nome_preview = str(instance.id)+"-preview%3d.png"
                arquivo_preview = pasta_sinal_preview+'/'+nome_preview
                subprocess.call("ffmpeg -i {0} -vf select='not(mod(n\,{1}))' -vsync vfr {2}".format(
                    arquivo_video_converter, duration, arquivo_preview), shell=True)
                # Atualiza path dos preview
                for i, preview in enumerate(preview_fields):
                    nome_relativo_preview = "sinal_preview/" + \
                        str(instance.id)+"-preview00"+str(i+1)+".png"
                    Sinal.objects.filter(id=instance.id).update(
                        **{"%s" % preview.field.name: nome_relativo_preview}
                    )

            if os.path.isfile(url_base+'/'+field.name):
                os.remove(url_base+'/'+field.name)
            if os.path.isfile(url_base+'/'+str(instance.videos_originais_converter[index])):
                os.remove(url_base+'/' +
                          str(instance.videos_originais_converter[index]))

        else:
            if field.name == '' and instance.videos_originais_converter[index] != '':
                os.remove(settings.MEDIA_ROOT+'/' +
                          str(instance.videos_originais_converter[index]))


def converter_todos(sinal_inicio=1):
    sinais = Sinal.objects.all()
    logging.basicConfig(filename=settings.MEDIA_ROOT+"/conversao.log", level=logging.INFO,
                        format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', datefmt='%Y/%m/%d-%H:%M:%S')
    log = logging.getLogger("conversao")

    for sinal in sinais:
        if(sinal.id < int(sinal_inicio)):
            continue
        url_base = settings.MEDIA_ROOT
        pasta_sinal_videos = '{0}/sinal_videos'.format(url_base)
        video_fields = [sinal.video_sinal, sinal.video_descricao,
                       sinal.video_exemplo, sinal.video_variacao]
        tags = ['sinal', 'descricao', 'exemplo', 'variacao']

        for index, field in enumerate(video_fields):
            if field:
                log.info(str(sinal.id) + '  ' + tags[index] + "- tem nome")
                if os.path.isfile(url_base+'/'+field.name):
                    log.info(str(sinal.id) + '  ' +
                             tags[index] + "- tem arquivo")
                    nome_video_converter = str(
                        sinal.id)+'-'+tags[index]+'-'+datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".mp4"
                    arquivo_video_converter = pasta_sinal_videos+'/'+nome_video_converter
                    log.info(str(sinal.id) + " convertendo " +
                             field.name + ' para '+arquivo_video_converter)
                    subprocess.call('ffmpeg -i {0}/{1} -y -hide_banner -nostats -c:v libx264 -crf 19 -movflags faststart -threads 0 -preset slow -an -strict -2 {2}'
                                    .format(
                                        url_base,
                                        field.name,
                                        arquivo_video_converter
                                    ), shell=True)
                    nome_relativo_arquivo_convertido = 'sinal_videos/'+nome_video_converter
                    Sinal.objects.filter(id=sinal.id).update(
                        **{"%s" % field.field.name: nome_relativo_arquivo_convertido})
                else:
                    log.info(str(sinal.id) + '  ' +
                             tags[index] + "- não tem arquivo")
