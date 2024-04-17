DISPLAY=

# all: clean prepare build run-broker delay30s run delay60s test

# delay30s:
# 	sleep 30

# delay60s:
# 	sleep 60

sys-packages:
	# sudo apt install -y docker-compose
	# sudo usermod -aG docker ${USER}
	sudo apt install python3-pip -y
	# WSL2 specific trick to prevent pip from hanging
	pip -v install pipenv

broker:
	docker-compose -f kafka/docker-compose.yaml up -d

pipenv:
	pipenv install -r requirements-dev.txt

prepare: sys-packages pipenv build run-broker

build:
	docker-compose build

run-broker:
	docker-compose up -d su-zookeeper su-broker

run: run-broker
	docker-compose up -d

# restart:
# 	docker-compose restart

# stop:
# 	docker-compose stop

# down:
# 	docker-compose down

# logs:
# 	docker-compose logs -f --tail 100

# clean:
# 	docker-compose down; pipenv --rm; rm -f Pipfile*; echo cleanup complete

# check_broker:
# 	# message broker needs to be reachable by name su-broker - it is expected so in tests
# 	ping -c 1 su-broker; if [ $$? -eq 0 ]; then echo "broker check ok" ; else echo "please add su-broker to your /etc/hosts" ; fi


# test: check_broker
# 	pipenv run pytest -sv --reruns 5