# build:
# 	sam build

deploy:
	echo 'Deploying'

tailEvents:
	echo 'Tailing events'

# sam build --use-container

freeze:
	poetry export --without-hashes -f requirements.txt --output ./lambdas/requirements.txt

build:
	sam build

invokeOrderCreatedEvent:
	sam local invoke OrderCreatedLambda
