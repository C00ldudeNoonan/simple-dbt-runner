# how to dbt

Gotta think a little about structure here. I think we need to have a setup script that takes some of the stuff here and puts it in the right place.

This is enough for local dev of a dbt project -> running `docker compose up` builds an image + container with dbt installed. You can then run `docker exec -it dbt_container_dbt_1 bash` to get a shell in the container and run dbt commands. You also need to have your credentials as local environment variables which can then be passed to the container.