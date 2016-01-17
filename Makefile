NAME=nomad-web

DOCKER_MACHINE_NAME := $(shell echo $${DOCKER_MACHINE_NAME:-default})
DOCKER_IP=$(shell docker-machine ip ${DOCKER_MACHINE_NAME})

help:
	# bootstrap - initial command that builds everything for development
	# build - initial command that builds everything
	# runserver - runs nomadboard
	# django-shell - runs django's shell

bootstrap:
	make build
	make wakeup-database
	make staticfiles

build:
	docker-compose build

runserver:
	@echo "==="
	@echo "Nomadboard is now running on $(DOCKER_IP):8000"
	@echo "==="
	# docker-compose run nomad-web django-admin runserver 0.0.0.0:8000
	docker-compose up

django:
	docker-compose run $(NAME) django-admin ${DJANGO_CMD}

django-shell:
	docker-compose run $(NAME) django-admin shell

bash-shell:
	docker-compose run $(NAME) bash

wakeup-database:
	docker-compose up -d nomad-db

migrations:
	docker-compose run $(NAME) django-admin makemigrations

migrate:
	docker-compose run $(NAME) django-admin migrate

collectstatic:
	docker-compose run $(NAME) django-admin collectstatic --noinput

superuser:
	docker-compose run $(NAME) django-admin createsuperuser

lint:
	flake8 .

clean-pyc:
	find . -name "*.pyc" -type f -delete

run-production:
	@echo "==="
	@echo "Run production!"
	@echo "==="
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

compile-staticfiles:
	docker-compose run nomad-grunt npm run-script grunt

staticfiles:
	make compile-staticfiles
	make collectstatic

grunt-watch:
	docker-compose run nomad-grunt npm run-script grunt watch
