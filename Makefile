NAME=nomad-web

help:
	# build - initial command that builds everything
	# runserver - runs nomadboard
	# django-shell - runs django's shell

# start: build wakeup-database migrate collectstatic

build:
	docker-compose build $(NAME)
	docker-compose build nomad-db
	docker-compose build nomad-grunt

runserver:
	@echo "==="
	@echo "Nomadboard is now running."
	@echo "==="
	docker-compose up

run-production:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

django:
	docker-compose run $(NAME) django-admin ${DJANGO_CMD}

django-shell:
	docker-compose run $(NAME) django-admin shell

wakeup-database:
	docker-compose up -d db

migrations:
	docker-compose run $(NAME) django-admin makemigrations

migrate:
	docker-compose run $(NAME) django-admin migrate

collectstatic:
	docker-compose run $(ADMIN_NAME) django-admin collectstatic --noinput

superuser:
	docker-compose run $(NAME) django-admin createsuperuser

test:
	docker-compose run \
		$(NAME) py.test -x --strict $${TEST_ARGS:-"tests/"}

lint-install:
	pip install -r lint-requirements.txt

lint:
	flake8 . --select=E,F,I,W

lint-diff:
	git diff upstream/master src tests | flake8 --select=E,F,I,W --diff

clean-pyc:
	find . -name "*.pyc" -type f -delete

docker-full-clean:
	@echo Removing all containers
	docker rm $(docker ps -a -q) -f

docker-clean-images:
	@echo Removing old images
	docker rmi $(docker images -q) -f

docker-clean: docker-full-clean docker-clean-images
