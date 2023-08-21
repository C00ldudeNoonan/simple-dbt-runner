# how to dbt

Gotta think a little about structure here. I think we need to have a setup script that takes some of the stuff here and puts it in the right place.

## Notes

- `run_dbt.sh` is what we want to run in prod. You can pass dbt commands to it as arguments. So eg a cron job could run `run_dbt.sh dbt run --select tag:daily_models` to run the daily models with the right tag.
- for local dev you want to run `docker compose up`. This starts the container and also runs `simplehttp.py` (tiny forever web server). You can then run `docker exec -it dbt_container_dbt_1 bash` to get a shell in the container and run dbt commands. You need to have your personal DWH creds as local env vars which will be passed to the container.

## TODO

- probably need to specify where the dbt project should go and restructure the directory
- probably need to add a part to run_dbt.sh that pulls secrets from AWS Secrets Manager and sets as env vars? Doesn't that end up being unsafe though? Not sure what to do about that, unless we can erase the env vars after they get passed to the container
- need to add a file where people can add cron jobs and have them get added to the crontab
- need to add GH Action to deploy to EC2 on merge to main. This should also probably update the crontab when that happens incase people add/remove cron jobs.

Completely missing anything RE: logging. Out of scope?