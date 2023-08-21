#!/bin/bash

# Build the image if it doesn't exist
if [[ "$(docker images -q dbt_container_dbt 2> /dev/null)" == "" ]]; then
  docker build --no-cache -t dbt_container_dbt .
fi

# Run the dbt commands
docker run -it dbt_container_dbt /bin/bash -c "cd /app && $@"
