
install:
	yarn

dev: install
	yarn dev

ready:
    docker run --rm --privileged linuxkit/binfmt:v0.8

tag:
	docker tag google-ddns registry.dougflynn.dev/heat-level .

build-arm: ready
	docker buildx build --platform linux/arm64 --push \
		-t registry.dougflynn.dev/heat-level \
		-f docker/Dockerfile \
		.