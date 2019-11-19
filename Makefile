PORT=8001

run-docker:
	docker build --tag streets-of-helsinki .
	docker run -it --env PORT=$(PORT) -p $(PORT):$(PORT) streets-of-helsinki

deploy-heroku:
	heroku container:push web
	heroku container:release web