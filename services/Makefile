build:
	docker build -t ynput/my-cool-service .

dev: build
	docker run --rm  -ti \
		--env AYON_API_KEY=veryinsecurapikey \
		--env AYON_SERVER_URL=http://192.168.51.184:5000 \
		--env AYON_ADDON_NAME=example \
		--env AYON_ADDON_VERSION=2.0.1+git \
		-v ./service:/service/service \
		ynput/my-cool-service
