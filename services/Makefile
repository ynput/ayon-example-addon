include .env

IMAGE_NAME=ynput/ayon-example-service

AYON_ADDON_NAME=example
AYON_ADDON_VERSION=$(shell cd .. && python -c "import package; print(f\"{package.version.split('-')[0]}+git\")")

build:
	docker build -t $(IMAGE_NAME) .

dev: build
	docker run --rm  -ti \
		--network host \
		--env AYON_API_KEY=$(AYON_API_KEY) \
		--env AYON_SERVER_URL=$(AYON_SERVER_URL) \
		--env AYON_ADDON_NAME=example \
		--env AYON_ADDON_VERSION=$(AYON_ADDON_VERSION) \
		-v ./service:/service/service \
		$(IMAGE_NAME)
