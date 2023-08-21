#!/bin/bash

# Run the Docker container
docker run -it dbt_container_dbt /bin/bash -c "cd /app && $@"
