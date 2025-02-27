# Stop and remove all containers
destroy:
	docker-compose down --remove-orphans --volumes

# Build and start all docker containers
start:
	docker-compose up --detach --build

# SSH into docker container by name.  Only generic shell (sh) is available.
open:
	docker-compose exec $(area) sh

# Displays status of containers
status:
	docker-compose ps

# View container logs by name.
logs:
	docker-compose logs $(area)

# Check packages for security vulnerabilities.
check-packages:
	docker-compose exec backend pip check

# Removes all docker resources.
nuke-it:
	docker-compose down --remove-orphans --volumes
	docker volume prune --force
	docker network prune --force
	docker container prune --force
	docker rmi -f $(shell docker images -aq)

# Removes unused docker resources
clean-images:
	# docker rmi $(shell docker images --filter dangling=true --quiet)
	docker system prune -f --volumes
