## Glossário Letras Libras UFSC

user: admin@admin.com  
senha: admin  

## Requisitos

```bash
$ pip install -r requirements.txt
$ sudo apt install ffmpeg
```

## Comandos úteis
Para fazer o dumpdata:

```python
./manage.py dumpdata --indent 4 --natural-foreign --natural-primary -e auth.permission -e contenttypes -e sessions -e admin  > glossario/fixtures/initial.json
```

Popular o banco de dados local (sqlite3): chamar o comando:

```python
./manage.py loaddata glossario/fixtures/initial.json
```

Docker e docker-compose:
Rodar todos os aplicativos, primeira vez é necessário a flag --build:

```bash
docker-compose up --build
```

Fecha e deleta todos os containers:

```bash
docker-compose down
```

Rodar comandos dentro de um container pelo shell

```bash
docker exec -it [CONTAINER NAME] /bin/bash
```

Rodar comandos dentro do container do Postgresql:

```bash
docker exec -it [container_name] psql -U [postgres_user]
```

Criar Extensão para o  MySQL

```bash
CREATE EXTENSION unaccent;
```

## Desenvolvimento
Desenvolvedor Ramon Dutra Miranda

Professores responseveis pela pesquisa:  
Janine Soares de Oliveira  
Marianne Rossi Stumpf

Bolsistas:  
Bryan Martins Lima

Equipe antiga:  
Cleberton de Souza Oliveira  
João Pedro Gutierrez Kieling Villegas  
Sabrina Hanich  
Thiago Brezinski  

Apoio institucional:  
Universidade Federal de Santa Catarina - UFSC  
Letras Libras UFSC  
NALS - UFSC

Este projeto inicia a nova fase do glossario.libras.ufsc.br  
Fique a vontade para compartilhar o conhecimento!  
:)  

Estamos usando Django 2.1.x e Python 3.x

Plataforma de Glossários Libras  
Um glossário que reunie glossários de varias areas do conhecimento humano.

- PGL
  - Um Glossário de determinada area
	- Sinais
  - Temas
	- Vinculados diretamente ao sinal

1.0 a versão interna do moodle, considerada pre-histórica

2.0 a versão glossário LETRAS Libras, que foi meu tcc focando o curso Letras Libras somente.

3.0 a versão que virou multi-glossarios, a atual em php e com mais de uma area do conhecimento.

4.0 Utilizando Python e Django, html5, multi-glossarios, multiareas, multitemas, pesquisas, mais moderno e dinamico para criar glossários e sinais.
