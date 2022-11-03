start-server:
	python -m server.api --port 8081

start-client:
	npm run serve --prefix client -- --port 8080

deploy-client:
	npm run build --prefix client
	cp -r client/dist ~/deployment/memit

deploy-server:
	cp -r server/ ~/deployment/memit/
	supervisorctl restart gunicorn
