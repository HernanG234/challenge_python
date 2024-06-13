.PHONY: test list init

# runs before build, it unmounts volumes as well
down:
	docker-compose down -v

# build is a helper to make it easy to build the docker container, it runs before
# any downstream step
build: down
	docker-compose build

# a wrapper for docker-compose up, runs an immutable instance of the app
up: build
	docker-compose up

# dev runs the container with a mounted volume to the code repo. In dev mode, it runs the
# container just like `up` but you can "live code" in the directory. Optionally, you drop into
# a shell in a dev container with `make exec`
dev:
	./scripts/container-run.sh

# exec is used in combination with a running continer. This allows you to drop into a shell for
# an active shell.
exec:
	./scripts/container-exec.sh

# shell is meant to give you a /bin/bash into the container with a mounted volume
# this allows for adminstrator of things such as poetry update and other administrative tasks
# in which you might want to mutate the state of files in your repo
shell:
	ENTRYPOINT=/bin/bash ./scripts/container-run.sh

# test is an immuatable pytest that is safe to run locally and in CI
test:
	ENTRYPOINT=pytest ./scripts/container-run.sh
