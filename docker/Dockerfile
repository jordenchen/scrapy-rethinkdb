FROM alpine:latest

ENV BUILD_PACKAGES build-base libxslt-dev libxml2-dev libffi-dev python-dev openssl-dev

RUN apk add --update python py-pip libxslt libxml2 make && rm -rf /var/cache/apk/*

RUN apk add --update ${BUILD_PACKAGES} && \
	pip --no-cache-dir install scrapy nose coverage mock rethinkdb && \
	apk del ${BUILD_PACKAGES} && \
	rm -rf /var/cache/apk/*

RUN mkdir -p /data