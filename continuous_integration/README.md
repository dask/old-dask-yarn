# Continious Integration

## Local test

Requirements:
-  `docker`
- `docker-compose`

Build the container:
```bash
docker build -t dask_yarn .
```

Start the container and wait for the it to be ready:

```bash
docker-compose up
```

To start a bash session in the running container:

```bash
# Get the container ID
export CONTAINER_ID=$(docker ps -l -q)

# Start the bash session
docker exec -it $CONTAINER_ID /bin/bash
```
