## Установка

### Локальная разработка

* git clone git@github.com:blupup-barcs/drf-pr.git 

* cd drf-project

* python -m venv venv

* source venv/bin/activate

* pip install -r requirements.txt

* cp .env.sample .env  
  (заполните переменные)

* python manage.py migrate

* python manage.py runserver

### Production-развертывание

#### На сервере выполните:

* sudo apt update && sudo apt install docker.io

* sudo systemctl enable docker

* mkdir -p ~/drf-project

* Скопируйте .env в ~/drf-project/.env



CI/CD Pipeline

Автоматически при push, pull_request:

* Собирает Docker-образ
* Пушит в Docker Hub
* Разворачивает на сервере через SSH

Необходимые Secrets:

* DOCKER_HUB_USERNAME
* DOCKER_HUB_TOKEN
* SSH_KEY
* SERVER_IP