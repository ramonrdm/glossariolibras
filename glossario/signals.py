from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from glossario.models import Glossario, Sinal, UserGlossario
from django.conf import settings
import subprocess
import datetime
import os, os.path

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

"""
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
"""

def converter_todos(sinal_inicio=1):
    sinais = Sinal.objects.all()
    import logging
    logging.basicConfig(filename=settings.MEDIA_ROOT+"/conversao.log", level=logging.INFO, 
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s', datefmt='%Y/%m/%d-%H:%M:%S')
    log = logging.getLogger("conversao")
    log.info("################  Começando  ################")

    for sinal in sinais:
        if(sinal.id < int(sinal_inicio)):
            print(" maior ###", sinal.id, sinal_inicio)
            continue
        url_base = settings.MEDIA_ROOT
        pasta_sinal_videos = '{0}/sinal_videos'.format(url_base)
        videoFields = [sinal.video_sinal, sinal.video_descricao, sinal.video_exemplo, sinal.video_variacao]
        tags = ['sinal', 'descricao', 'exemplo', 'variacao']

        for index, field in enumerate(videoFields):
            if field:
                log.info(str(sinal.id)+ '  ' + tags[index] +"- tem nome")
                if os.path.isfile(url_base+'/'+field.name):
                    log.info(str(sinal.id)+ '  ' + tags[index] +"- tem arquivo")
                    nome_video_converter = str(sinal.id)+'-'+tags[index]+'-'+datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".mp4"
                    arquivo_video_converter = pasta_sinal_videos+'/'+nome_video_converter
                    log.info(str(sinal.id)+ " convertendo " + field.name +' para '+arquivo_video_converter)
                    subprocess.call('ffmpeg -i {0}/{1} -y -hide_banner -nostats -c:v libx264 -crf 19 -movflags faststart -threads 0 -preset slow -an -strict -2 {2}'
                        .format(
                            url_base,
                            field.name,
                            arquivo_video_converter
                            ),shell=True)
                    log.info("############# VIDEO CONVERTIDO ###############")
                    nome_relativo_arquivo_convertido = 'sinal_videos/'+nome_video_converter
                    Sinal.objects.filter(id=sinal.id).update(**{"%s" % field.field.name: nome_relativo_arquivo_convertido} )
                else:
                    log.info(str(sinal.id)+ '  ' + tags[index] +"- não tem arquivo")

    log.info("################### terminou  ################")

def change_video_names():
    import json
    j = """[{"id":"692","video_original":"692-04-23-15-21-25.mp4","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"693","video_original":"693-04-23-15-24-47.mp4","video_original_definicao":"d-693-12-04-12-52-10.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"694","video_original":"694-04-23-15-27-08.mp4","video_original_definicao":"d-694-12-04-12-49-12.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"695","video_original":"695-04-23-15-36-03.mp4","video_original_definicao":"d-695-12-04-12-50-59.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"696","video_original":"696-04-23-15-38-41.mp4","video_original_definicao":"d-696-12-04-12-53-50.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"697","video_original":"697-04-23-15-44-32.mp4","video_original_definicao":"d-697-12-04-13-34-34.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"698","video_original":"698-04-23-15-47-00.mp4","video_original_definicao":"d-698-12-04-13-36-52.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"699","video_original":"699-04-23-15-51-13.mp4","video_original_definicao":"d-699-12-20-17-15-00.mov","video_original_exemplo":"e-699-12-20-17-15-15.mov","video_original_variacoes":""},
            {"id":"700","video_original":"700-04-23-15-56-30.mp4","video_original_definicao":"d-700-12-04-12-53-11.mp4","video_original_exemplo":"","video_original_variacoes":"v-700-04-23-15-56-35.mp4"},
            {"id":"701","video_original":"701-04-23-15-59-54.mp4","video_original_definicao":"d-701-06-04-01-20-58.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"702","video_original":"702-04-23-16-02-16.mp4","video_original_definicao":"d-702-12-04-13-30-46.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"703","video_original":"703-04-23-16-07-00.mp4","video_original_definicao":"d-703-12-10-19-53-28.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"704","video_original":"704-04-23-16-09-17.mp4","video_original_definicao":"d-704-12-04-13-30-14.mp4","video_original_exemplo":"e-704-12-20-16-32-31.mp4","video_original_variacoes":""},
            {"id":"705","video_original":"705-04-23-16-12-28.mp4","video_original_definicao":"d-705-12-04-13-29-00.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"706","video_original":"706-04-23-16-16-10.mp4","video_original_definicao":"d-706-12-04-12-53-30.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"707","video_original":"707-04-23-16-18-07.mp4","video_original_definicao":"d-707-06-07-22-09-16.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"708","video_original":"708-04-23-16-22-21.mp4","video_original_definicao":"d-708-05-16-04-27-03.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"709","video_original":"709-04-23-16-26-54.mp4","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"710","video_original":"710-04-23-16-32-48.mp4","video_original_definicao":"d-710-12-04-12-42-47.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"711","video_original":"711-04-23-16-34-22.mp4","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"712","video_original":"712-04-23-16-39-01.mp4","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"713","video_original":"713-04-23-16-39-45.mp4","video_original_definicao":"d-713-06-07-22-17-02.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"714","video_original":"714-04-23-16-42-21.mp4","video_original_definicao":"d-714-12-04-12-40-30.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"715","video_original":"715-04-23-16-43-59.mp4","video_original_definicao":"d-715-12-04-12-42-32.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"716","video_original":"716-04-23-16-46-31.mp4","video_original_definicao":"d-716-12-04-12-47-28.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"717","video_original":"717-04-23-16-48-36.mp4","video_original_definicao":"d-717-06-07-22-18-18.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"718","video_original":"718-04-23-16-52-15.mp4","video_original_definicao":"d-718-05-26-18-50-42.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"719","video_original":"719-04-23-16-57-06.mp4","video_original_definicao":"d-719-06-04-01-32-59.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"720","video_original":"720-04-23-16-58-30.mp4","video_original_definicao":"d-720-12-04-13-09-13.mp4","video_original_exemplo":"e-720-12-04-13-09-33.mp4","video_original_variacoes":"v-720-04-23-16-58-34.mp4"},
            {"id":"721","video_original":"721-04-23-17-04-27.mp4","video_original_definicao":"d-721-12-04-12-51-23.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"722","video_original":"722-04-23-17-04-41.mp4","video_original_definicao":"d-722-06-04-02-07-55.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"723","video_original":"723-04-23-17-08-37.mp4","video_original_definicao":"d-723-06-04-02-08-22.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"724","video_original":"724-04-23-17-09-34.mp4","video_original_definicao":"d-724-12-04-12-46-25.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"725","video_original":"725-04-23-17-12-26.mp4","video_original_definicao":"d-725-06-07-22-20-06.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"726","video_original":"726-04-23-17-18-41.mp4","video_original_definicao":"d-726-05-16-04-10-18.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"727","video_original":"727-04-23-17-19-43.mp4","video_original_definicao":"d-727-12-04-13-14-09.mp4","video_original_exemplo":"e-727-12-04-13-26-42.mp4","video_original_variacoes":""},
            {"id":"728","video_original":"728-04-23-17-22-40.mp4","video_original_definicao":"d-728-05-16-04-20-11.mov","video_original_exemplo":"","video_original_variacoes":"v-728-04-23-17-22-47.mp4"},
            {"id":"729","video_original":"","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"730","video_original":"730-06-04-13-36-23.mp4","video_original_definicao":"d-730-06-04-13-36-26.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"731","video_original":"731-06-04-13-45-06.mp4","video_original_definicao":"d-731-06-04-13-45-09.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"732","video_original":"732-06-04-13-51-27.mp4","video_original_definicao":"d-732-06-04-13-51-40.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"733","video_original":"733-06-04-14-03-06.mp4","video_original_definicao":"d-733-06-04-14-03-08.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"734","video_original":"734-06-04-14-09-29.mp4","video_original_definicao":"d-734-06-04-14-09-34.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"735","video_original":"735-06-04-14-44-31.mp4","video_original_definicao":"d-735-06-04-14-44-34.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"736","video_original":"736-06-04-14-46-50.mp4","video_original_definicao":"d-736-06-04-14-46-53.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"737","video_original":"737-06-04-14-52-01.mp4","video_original_definicao":"d-737-06-04-14-52-03.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"738","video_original":"738-06-04-14-55-27.mp4","video_original_definicao":"d-738-06-04-14-55-29.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"739","video_original":"739-06-04-14-59-33.mp4","video_original_definicao":"d-739-06-04-14-59-36.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"740","video_original":"740-06-04-15-03-01.mp4","video_original_definicao":"d-740-06-04-15-03-03.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"741","video_original":"741-06-04-15-05-06.mp4","video_original_definicao":"d-741-06-04-15-05-08.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"742","video_original":"742-06-04-15-08-41.mp4","video_original_definicao":"d-742-06-04-15-08-44.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"743","video_original":"743-06-04-15-13-08.mp4","video_original_definicao":"d-743-06-04-15-13-16.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"744","video_original":"744-06-04-15-21-18.mp4","video_original_definicao":"d-744-06-04-15-21-26.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"745","video_original":"745-06-04-15-27-33.mp4","video_original_definicao":"d-745-06-04-15-27-41.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"746","video_original":"746-06-04-16-05-50.mp4","video_original_definicao":"d-746-06-04-16-05-59.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"747","video_original":"747-06-04-16-27-12.mp4","video_original_definicao":"d-747-06-04-16-27-16.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"748","video_original":"748-06-04-16-32-27.mp4","video_original_definicao":"d-748-06-04-16-32-30.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"749","video_original":"749-06-04-16-34-27.mp4","video_original_definicao":"d-749-06-04-16-34-30.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"750","video_original":"750-06-04-16-38-38.mp4","video_original_definicao":"d-750-06-04-16-38-43.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"751","video_original":"751-06-04-16-49-00.mp4","video_original_definicao":"d-751-06-04-16-49-05.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"752","video_original":"752-06-04-16-52-27.mp4","video_original_definicao":"d-752-06-04-16-52-31.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"753","video_original":"753-06-04-19-51-25.mp4","video_original_definicao":"d-753-06-04-19-51-29.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"754","video_original":"754-06-04-19-54-31.mp4","video_original_definicao":"d-754-06-04-19-54-37.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"755","video_original":"755-06-05-19-25-40.mp4","video_original_definicao":"d-755-06-05-19-25-50.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"756","video_original":"756-06-05-19-29-44.mp4","video_original_definicao":"d-756-06-05-19-29-49.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"757","video_original":"757-06-05-19-32-18.mp4","video_original_definicao":"d-757-06-05-19-32-26.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"758","video_original":"758-06-05-19-34-24.mp4","video_original_definicao":"d-758-06-05-19-34-29.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"759","video_original":"759-06-05-19-39-11.mp4","video_original_definicao":"d-759-06-05-19-39-18.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"760","video_original":"760-06-05-19-45-42.mp4","video_original_definicao":"d-760-06-05-19-45-47.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"761","video_original":"761-06-05-19-47-50.mp4","video_original_definicao":"d-761-06-05-19-47-57.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"762","video_original":"762-06-05-19-52-27.mp4","video_original_definicao":"d-762-06-05-19-52-33.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"763","video_original":"763-06-05-19-53-55.mp4","video_original_definicao":"d-763-06-05-19-53-59.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"764","video_original":"764-06-05-19-56-14.mp4","video_original_definicao":"d-764-06-05-19-56-21.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"765","video_original":"765-06-05-19-58-55.mp4","video_original_definicao":"d-765-06-05-19-59-02.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"766","video_original":"766-06-05-20-00-58.mp4","video_original_definicao":"d-766-06-05-20-01-03.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"767","video_original":"767-06-05-20-04-11.mp4","video_original_definicao":"d-767-06-05-20-04-17.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"768","video_original":"768-06-05-20-07-07.mp4","video_original_definicao":"d-768-06-05-20-07-14.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"769","video_original":"769-06-05-20-12-44.mp4","video_original_definicao":"d-769-06-05-20-12-49.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"770","video_original":"770-06-05-20-16-26.mp4","video_original_definicao":"d-770-06-05-20-16-33.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"771","video_original":"771-06-07-15-02-40.mp4","video_original_definicao":"d-771-06-07-15-02-47.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"772","video_original":"772-06-07-15-05-43.mp4","video_original_definicao":"d-772-06-07-15-05-49.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"773","video_original":"773-06-07-15-24-20.mp4","video_original_definicao":"d-773-06-07-15-24-25.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"774","video_original":"774-06-07-15-27-11.mp4","video_original_definicao":"d-774-06-07-15-27-14.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"775","video_original":"775-06-07-15-29-05.mp4","video_original_definicao":"d-775-06-07-15-29-09.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"776","video_original":"776-06-07-15-31-13.mp4","video_original_definicao":"d-776-06-07-15-31-18.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"777","video_original":"777-06-07-15-32-38.mp4","video_original_definicao":"d-777-06-07-15-32-41.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"778","video_original":"778-06-07-23-30-13.mp4","video_original_definicao":"d-778-05-26-18-47-51.mp4","video_original_exemplo":"e-778-05-26-18-48-12.mp4","video_original_variacoes":""},
            {"id":"779","video_original":"779-06-07-23-34-09.mp4","video_original_definicao":"d-779-10-22-01-09-23.mov","video_original_exemplo":"","video_original_variacoes":"v-779-06-07-23-34-19.mp4"},
            {"id":"780","video_original":"780-06-07-23-34-52.mp4","video_original_definicao":"d-780-10-22-01-12-04.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"781","video_original":"","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"782","video_original":"","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"783","video_original":"783-06-08-00-20-37.mp4","video_original_definicao":"d-783-10-22-01-12-22.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"784","video_original":"784-06-08-00-21-46.mp4","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"785","video_original":"785-06-08-00-22-38.mp4","video_original_definicao":"d-785-10-22-01-32-31.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"786","video_original":"786-06-08-00-23-41.mp4","video_original_definicao":"d-786-05-26-18-54-06.mp4","video_original_exemplo":"e-786-12-10-19-03-19.mov","video_original_variacoes":""},
            {"id":"787","video_original":"787-06-08-00-24-42.mp4","video_original_definicao":"d-787-10-22-01-12-30.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"788","video_original":"788-06-08-00-26-13.mp4","video_original_definicao":"d-788-12-10-12-11-09.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"789","video_original":"789-06-08-00-27-03.mp4","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"790","video_original":"790-06-08-00-27-46.mp4","video_original_definicao":"d-790-10-22-01-12-56.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"791","video_original":"791-06-08-00-29-58.mp4","video_original_definicao":"d-791-05-16-03-54-38.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"792","video_original":"792-06-08-00-31-32.mp4","video_original_definicao":"d-792-10-22-01-17-40.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"793","video_original":"793-06-08-00-34-48.mp4","video_original_definicao":"d-793-10-22-01-13-19.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"794","video_original":"794-06-08-00-37-58.mp4","video_original_definicao":"d-794-10-22-01-13-46.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"795","video_original":"795-06-08-00-39-37.mp4","video_original_definicao":"d-795-10-22-01-14-27.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"796","video_original":"796-06-08-00-40-33.mp4","video_original_definicao":"d-796-10-22-01-31-42.mov","video_original_exemplo":"e-796-12-26-13-46-54.jpg","video_original_variacoes":""},
            {"id":"797","video_original":"797-06-08-00-41-39.mp4","video_original_definicao":"d-797-10-22-01-14-48.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"798","video_original":"798-12-10-20-04-11.mp4","video_original_definicao":"d-798-06-02-04-08-07.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"799","video_original":"799-12-10-20-03-28.mp4","video_original_definicao":"d-799-08-12-03-50-25.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"800","video_original":"800-12-10-20-13-33.mp4","video_original_definicao":"d-800-06-02-04-24-05.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"801","video_original":"801-12-10-20-14-16.mp4","video_original_definicao":"d-801-06-02-04-34-16.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"802","video_original":"802-12-10-20-15-10.mp4","video_original_definicao":"d-802-06-02-04-42-41.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"803","video_original":"803-12-10-20-16-22.mp4","video_original_definicao":"d-803-06-02-04-45-31.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"804","video_original":"804-12-10-20-17-27.mp4","video_original_definicao":"d-804-06-02-04-48-56.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"805","video_original":"805-12-10-20-20-57.mp4","video_original_definicao":"d-805-07-01-19-39-32.mp4","video_original_exemplo":"e-805-07-01-19-43-37.mp4","video_original_variacoes":""},
            {"id":"806","video_original":"806-12-10-20-22-15.mp4","video_original_definicao":"d-806-07-01-19-26-55.mp4","video_original_exemplo":"e-806-07-01-19-23-52.mp4","video_original_variacoes":""},
            {"id":"807","video_original":"807-12-10-20-22-59.mp4","video_original_definicao":"d-807-07-12-23-34-51.mp4","video_original_exemplo":"e-807-07-01-20-44-18.mp4","video_original_variacoes":""},
            {"id":"808","video_original":"808-12-10-20-23-31.mp4","video_original_definicao":"d-808-07-01-19-14-02.mp4","video_original_exemplo":"e-808-07-01-19-14-13.mp4","video_original_variacoes":""},
            {"id":"809","video_original":"809-12-10-20-24-04.mp4","video_original_definicao":"d-809-06-04-01-19-44.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"810","video_original":"810-12-10-20-24-34.mp4","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"811","video_original":"811-12-10-20-25-19.mp4","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"812","video_original":"812-12-10-20-26-15.mp4","video_original_definicao":"d-812-07-01-05-54-44.mp4","video_original_exemplo":"e-812-07-01-05-55-14.mp4","video_original_variacoes":""},
            {"id":"813","video_original":"813-12-10-20-26-58.mp4","video_original_definicao":"d-813-07-01-05-44-09.mp4","video_original_exemplo":"e-813-07-01-05-44-23.mp4","video_original_variacoes":""},
            {"id":"814","video_original":"814-12-10-20-27-42.mp4","video_original_definicao":"d-814-07-12-23-29-48.mp4","video_original_exemplo":"e-814-07-01-20-39-32.mp4","video_original_variacoes":""},
            {"id":"815","video_original":"815-06-15-03-07-48.mp4","video_original_definicao":"d-815-07-12-23-32-04.mp4","video_original_exemplo":"e-815-07-01-20-40-26.mp4","video_original_variacoes":""},
            {"id":"816","video_original":"816-12-10-20-29-13.mp4","video_original_definicao":"d-816-08-12-03-45-43.mp4","video_original_exemplo":"e-816-07-01-20-42-08.mp4","video_original_variacoes":""},
            {"id":"817","video_original":"817-12-10-20-29-50.mp4","video_original_definicao":"d-817-07-01-19-53-06.mp4","video_original_exemplo":"e-817-07-01-19-54-11.mp4","video_original_variacoes":""},
            {"id":"818","video_original":"818-12-10-20-30-24.mp4","video_original_definicao":"d-818-07-01-19-56-29.mp4","video_original_exemplo":"e-818-07-01-20-07-14.mp4","video_original_variacoes":""},
            {"id":"819","video_original":"819-12-10-20-31-00.mp4","video_original_definicao":"d-819-07-12-23-38-05.mp4","video_original_exemplo":"e-819-07-01-20-43-06.mp4","video_original_variacoes":""},
            {"id":"820","video_original":"820-12-10-20-31-41.mp4","video_original_definicao":"d-820-07-01-20-15-08.mp4","video_original_exemplo":"e-820-07-01-20-16-44.mp4","video_original_variacoes":""},
            {"id":"821","video_original":"821-12-10-20-32-11.mp4","video_original_definicao":"d-821-07-12-23-37-03.mp4","video_original_exemplo":"e-821-07-01-20-43-54.mp4","video_original_variacoes":""},
            {"id":"822","video_original":"822-12-10-20-35-00.mp4","video_original_definicao":"d-822-06-14-14-33-11.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"823","video_original":"823-12-10-20-36-22.mp4","video_original_definicao":"d-823-06-14-19-10-59.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"824","video_original":"824-12-10-20-37-29.mp4","video_original_definicao":"d-824-06-14-15-39-28.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"825","video_original":"825-12-10-20-38-02.mp4","video_original_definicao":"d-825-06-14-15-42-00.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"826","video_original":"826-12-10-20-38-54.mp4","video_original_definicao":"d-826-06-14-16-04-04.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"827","video_original":"827-12-10-20-39-21.mp4","video_original_definicao":"d-827-06-14-16-06-22.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"828","video_original":"828-12-10-20-40-10.mp4","video_original_definicao":"d-828-06-14-16-09-55.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"829","video_original":"829-03-14-00-37-45.mp4","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"830","video_original":"","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"831","video_original":"831-03-14-15-15-21.mp4","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"832","video_original":"832-04-30-18-33-20.mp4","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"833","video_original":"833-05-16-01-08-47.mov","video_original_definicao":"d-833-05-26-19-43-00.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"834","video_original":"834-05-16-01-14-41.mov","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"835","video_original":"835-05-16-01-23-58.mov","video_original_definicao":"d-835-05-26-19-44-41.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"836","video_original":"836-05-16-03-47-01.mov","video_original_definicao":"d-836-05-26-19-46-13.mp4","video_original_exemplo":"e-836-01-16-06-20-27.mp4","video_original_variacoes":""},
            {"id":"837","video_original":"837-05-16-04-02-46.mp4","video_original_definicao":"d-837-07-01-20-28-23.mp4","video_original_exemplo":"e-837-07-01-20-21-25.mp4","video_original_variacoes":""},
            {"id":"838","video_original":"838-05-16-04-15-34.mov","video_original_definicao":"d-838-05-26-18-56-07.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"839","video_original":"839-05-16-04-32-55.mov","video_original_definicao":"d-839-05-26-19-46-34.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"840","video_original":"840-05-30-16-24-47.mp4","video_original_definicao":"d-840-07-01-05-38-26.mp4","video_original_exemplo":"e-840-07-01-05-38-57.mp4","video_original_variacoes":""},
            {"id":"841","video_original":"841-05-30-16-35-13.mp4","video_original_definicao":"d-841-07-01-19-20-28.mp4","video_original_exemplo":"e-841-07-01-19-21-17.mp4","video_original_variacoes":""},
            {"id":"842","video_original":"842-05-30-16-42-14.mp4","video_original_definicao":"d-842-06-04-01-53-22.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"843","video_original":"843-05-30-16-48-00.mp4","video_original_definicao":"d-843-06-14-00-06-44.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"844","video_original":"844-05-30-16-55-08.mp4","video_original_definicao":"d-844-07-01-19-49-14.mp4","video_original_exemplo":"e-844-07-01-19-42-47.mp4","video_original_variacoes":""},
            {"id":"845","video_original":"845-05-30-18-03-02.mp4","video_original_definicao":"d-845-08-12-03-48-11.mp4","video_original_exemplo":"e-845-08-12-03-48-32.mp4","video_original_variacoes":""},
            {"id":"846","video_original":"846-05-30-18-12-55.mp4","video_original_definicao":"d-846-06-04-00-32-33.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"847","video_original":"847-05-30-18-19-47.mp4","video_original_definicao":"d-847-06-04-00-33-37.mp4","video_original_exemplo":"e-847-06-04-00-33-46.mp4","video_original_variacoes":""},
            {"id":"848","video_original":"848-05-30-18-28-08.mp4","video_original_definicao":"d-848-07-12-23-31-27.mp4","video_original_exemplo":"e-848-07-01-20-39-06.mp4","video_original_variacoes":""},
            {"id":"849","video_original":"849-05-30-18-37-27.mp4","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"850","video_original":"850-05-30-18-41-08.mp4","video_original_definicao":"d-850-06-04-00-38-21.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"851","video_original":"851-05-30-18-49-06.mp4","video_original_definicao":"d-851-06-04-00-38-36.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"852","video_original":"852-05-30-18-53-30.mp4","video_original_definicao":"d-852-06-04-00-39-16.mp4","video_original_exemplo":"","video_original_variacoes":"v-852-12-20-17-47-56.mp4"},
            {"id":"853","video_original":"853-05-30-18-56-59.mp4","video_original_definicao":"d-853-06-14-00-03-09.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"854","video_original":"854-05-30-19-02-13.mp4","video_original_definicao":"d-854-07-12-23-35-05.mp4","video_original_exemplo":"e-854-07-01-20-42-18.mp4","video_original_variacoes":""},
            {"id":"855","video_original":"855-05-30-19-08-10.mp4","video_original_definicao":"d-855-06-04-01-13-04.mov","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"856","video_original":"856-05-30-19-13-11.mp4","video_original_definicao":"d-856-06-04-01-09-29.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"857","video_original":"857-05-30-19-20-41.mp4","video_original_definicao":"d-857-06-04-01-11-32.mov","video_original_exemplo":"","video_original_variacoes":"v-857-12-20-16-49-03.mp4"},
            {"id":"858","video_original":"858-06-03-17-21-27.mp4","video_original_definicao":"d-858-07-01-19-09-37.mp4","video_original_exemplo":"e-858-07-01-20-08-07.mp4","video_original_variacoes":""},
            {"id":"859","video_original":"859-06-03-17-22-08.mp4","video_original_definicao":"d-859-06-14-00-04-40.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"860","video_original":"860-06-03-17-22-44.mp4","video_original_definicao":"d-860-07-01-20-11-21.mp4","video_original_exemplo":"e-860-07-01-20-10-23.mp4","video_original_variacoes":""},
            {"id":"861","video_original":"861-06-03-17-01-56.mp4","video_original_definicao":"d-861-06-04-01-28-57.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"862","video_original":"862-06-03-17-03-36.mp4","video_original_definicao":"d-862-06-04-01-27-23.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"863","video_original":"863-06-03-17-05-26.mp4","video_original_definicao":"d-863-06-14-00-01-01.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"864","video_original":"864-06-03-17-06-47.mp4","video_original_definicao":"d-864-07-12-23-36-53.mp4","video_original_exemplo":"e-864-07-01-20-49-02.mp4","video_original_variacoes":""},
            {"id":"865","video_original":"865-06-03-17-07-53.mp4","video_original_definicao":"d-865-07-01-20-30-34.mp4","video_original_exemplo":"e-865-07-01-20-47-26.mp4","video_original_variacoes":""},
            {"id":"866","video_original":"866-06-03-17-09-41.mp4","video_original_definicao":"d-866-06-04-01-34-58.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"867","video_original":"867-06-03-17-14-17.mp4","video_original_definicao":"d-867-07-01-20-32-50.mp4","video_original_exemplo":"e-867-07-01-20-34-16.mp4","video_original_variacoes":""},
            {"id":"868","video_original":"868-06-03-17-15-23.mp4","video_original_definicao":"d-868-07-01-20-35-46.mp4","video_original_exemplo":"e-868-07-01-20-35-55.mp4","video_original_variacoes":""},
            {"id":"869","video_original":"869-06-03-17-17-01.mp4","video_original_definicao":"d-869-06-04-01-35-41.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"870","video_original":"870-06-03-17-19-00.mp4","video_original_definicao":"d-870-06-04-01-37-10.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"871","video_original":"871-06-03-17-20-46.mp4","video_original_definicao":"d-871-06-04-01-54-26.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"872","video_original":"872-06-15-03-06-07.mp4","video_original_definicao":"d-872-06-15-03-57-19.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"873","video_original":"873-06-15-03-16-57.mp4","video_original_definicao":"d-873-12-20-15-16-13.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"874","video_original":"874-07-13-20-14-15.mov","video_original_definicao":"d-874-07-17-02-29-29.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"875","video_original":"875-07-13-20-18-42.mov","video_original_definicao":"d-875-07-17-02-22-12.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"876","video_original":"876-07-13-20-24-18.mov","video_original_definicao":"","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"877","video_original":"877-07-13-20-29-09.mov","video_original_definicao":"d-877-07-17-02-24-51.mp4","video_original_exemplo":"","video_original_variacoes":""},
            {"id":"878","video_original":"878-07-13-20-32-17.mov","video_original_definicao":"d-878-07-17-02-40-11.mp4","video_original_exemplo":"","video_original_variacoes":""}]
            """
    sinais = json.loads(j)   
    for s in sinais:
        print('id: ' + s['id'])
        if s['video_original'] != "":
            Sinal.objects.filter(id=s["id"]).update(**{"%s" % 'video_sinal': s['video_original']} )
            print('video_sinal '+s['video_original'])
        if s['video_original_definicao'] != "":
            Sinal.objects.filter(id=s["id"]).update(**{"%s" % 'video_descricao': s['video_original_definicao']} )
            print('video_descricao '+s['video_original_definicao'])
        if s['video_original_exemplo'] != "":
            Sinal.objects.filter(id=s["id"]).update(**{"%s" % 'video_exemplo': s['video_original_exemplo']} )
            print('video_exemplo '+s['video_original_exemplo'])
        if s['video_original_variacoes'] != "":
            Sinal.objects.filter(id=s["id"]).update(**{"%s" % 'video_variacao': s['video_original_variacoes']} )
            print('video_variacao '+s['video_original_variacoes'])
        
        print('-')
    print("fim for...")




