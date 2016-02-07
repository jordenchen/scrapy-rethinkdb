
dev-env-create:
	docker build -t 'ownport/scrapy-rethinkdb:dev' --build-arg http_proxy=http://172.17.0.2:8118 docker/
	# docker build -t 'ownport/scrapy-rethinkdb:dev' docker/


dev-env-run:
	docker run -ti --rm --name scrapy-rethinkdb-dev-env \
		-v $(shell pwd):/data \
		-v $(shell pwd)/docker/scripts/run-as.sh:/usr/local/sbin/run-as.sh \
		ownport/scrapy-rethinkdb:dev \
		/usr/local/sbin/run-as.sh dev 1000 /bin/sh

dev-env-remove:
	docker rmi ownport/scrapy-rethinkdb:dev

test-all:
	nosetests

test-all-with-coverage:
	nosetests --with-coverage



