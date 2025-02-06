celery: 
	celery -A PROJECT worker -l INFO

deploy:
	kubectl create secret generic shop-api-secret --from-env-file=.env --dry-run=client -o yaml > secret.yml
	kubectl apply -f secret.yml
	kubectl apply -f deployment.yml
	kubectl set image deployment/shop-api shop-api=faraji88/shop-api:master
	kubectl rollout restart deployment shop-api
