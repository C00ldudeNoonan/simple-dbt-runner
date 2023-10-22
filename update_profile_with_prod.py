import sys
import ruamel.yaml

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True

workflow_jobs = {
    'run_dbt.yml': 'run_dbt',
    'run_dbt_force.yml': 'run_dbt',
    'run_dbt_on_cron.yml': 'dbt_scheduled_run',
    'run_incremental_dbt_on_merge.yml': 'dbt_run_on_merge_incremental',
    'run_dbt_on_pr.yml' : 'dbt_run_on_pr',
    'run_dbt_cleanup.yml' : 'dbt_run_cleanup'
}

# Load the profiles.yml file
with open('project_goes_here/profiles.yml', 'r') as f:
    profiles = yaml.load(f)

# get the profile name from dbt_project.yml
with open('project_goes_here/dbt_project.yml', 'r') as f:
    dbt_project = yaml.load(f)
    profile_name = dbt_project['profile']

# Get the type of datawarehouse we are using
dwh_type = sys.argv[1]
print("dwh_type: ", dwh_type)

# Add a new target called "prod" based on the type of datawarehouse
if dwh_type == 'postgres':
    profiles[profile_name]['outputs']['prod'] = {
        'type': 'postgres',
        'host': '{{ env_var("HOST") }}',
        'user': '{{ env_var("USERNAME") }}',
        'password': '{{ env_var("PASSWORD") }}',
        'port': '{{ env_var("PORT") | int }}',
        'dbname': '{{ env_var("DATABASE") }}',
        'schema': '{{ env_var("SCHEMA") }}',
        'threads': 8
    }

    # update the gh actions jobs
    for file, job in workflow_jobs.items():
        with open('.github/workflows/'+file, 'r') as f:
            data = yaml.load(f)

        # edit the env block for all the jobs
        data['jobs'][job]['env'] = {
            'HOST': '${{ secrets.HOST }}',
            'DATABASE': '${{ secrets.DATABASE }}',
            'USERNAME': '${{ secrets.USERNAME }}',
            'PASSWORD': '${{ secrets.PASSWORD }}',
            'PORT': '${{ secrets.PORT }}',
            'SCHEMA': '${{ secrets.SCHEMA }}'
        }

        with open('.github/workflows/'+file, 'w') as f:
            yaml.dump(data, f)

elif dwh_type == 'snowflake':
    profiles[profile_name]['outputs']['prod'] = {
        'type': 'snowflake',
        'account': '{{ env_var("SNOWFLAKE_ACCOUNT") }}',
        'role': '{{ env_var("SNOWFLAKE_ROLE") }}',
        'user': '{{ env_var("USERNAME") }}',
        'password': '{{ env_var("PASSWORD") }}',
        'database': '{{ env_var("DATABASE") }}',
        'schema': '{{ env_var("SCHEMA") }}',
        'warehouse': '{{ env_var("WAREHOUSE") }}',
        'threads': 8
    }

    # update the gh actions jobs
    for file, job in workflow_jobs.items():
        with open('.github/workflows/'+file, 'r') as f:
            data = yaml.load(f)

        # edit the env block for all the jobs
        data['jobs'][job]['env'] = {
            'SNOWFLAKE_ACCOUNT': '${{ secrets.SNOWFLAKE_ACCOUNT }}',
            'DATABASE': '${{ secrets.DATABASE }}',
            'SNOWFLAKE_ROLE': '${{ secrets.SNOWFLAKE_ROLE }}',
            'USERNAME': '${{ secrets.USERNAME }}',
            'PASSWORD': '${{ secrets.PASSWORD }}',
            'SCHEMA': '${{ secrets.SCHEMA }}',
            'WAREHOUSE': '${{ secrets.WAREHOUSE }}',
        }

        with open('.github/workflows/'+file, 'w') as f:
            yaml.dump(data, f)

elif dwh_type == 'redshift':
    profiles[profile_name]['outputs']['prod'] = {
        'type': 'redshift',
        'host': '{{ env_var("HOST") }}',
        'user': '{{ env_var("USERNAME") }}',
        'password': '{{ env_var("PASSWORD") }}',
        'port': '{{ env_var("PORT") | int }}',
        'dbname': '{{ env_var("DATABASE") }}',
        'schema': '{{ env_var("SCHEMA") }}',
        'threads': 8
    }

    # update the gh actions jobs
    for file, job in workflow_jobs.items():
        with open('.github/workflows/'+file, 'r') as f:
            data = yaml.load(f)

        # edit the env block for all the jobs
        data['jobs'][job]['env'] = {
            'HOST': '${{ secrets.HOST }}',
            'USERNAME': '${{ secrets.USERNAME }}',
            'PASSWORD': '${{ secrets.PASSWORD }}',
            'PORT': '${{ secrets.PORT }}',
            'DATABASE': '${{ secrets.DATABASE }}',
            'SCHEMA': '${{ secrets.SCHEMA }}',
        }

        with open('.github/workflows/'+file, 'w') as f:
            yaml.dump(data, f)

elif dwh_type == 'bigquery':
    profiles[profile_name]['outputs']['prod'] = {
        'type': 'bigquery',
        'method': 'oauth',
        'project': '{{ env_var("PROJECT_NAME") }}',
        'dataset': '{{ env_var("DATASET") }}',
        'threads': 8
    }


            # update the gh actions jobs
    for file, job in workflow_jobs.items():
        with open('.github/workflows/'+file, 'r') as f:
            data = yaml.load(f)

        # edit the env block for all the jobs
        data['jobs'][job]['env'] = {
            'PROJECT_NAME': '${{ secrets.PROJECT_NAME }}',
            'DATASET': '${{ secrets.DATASET }}',
        }

        with open('.github/workflows/'+file, 'w') as f:
            yaml.dump(data, f)

# Save the updated profiles.yml file
with open('project_goes_here/profiles.yml', 'w') as f:
    yaml.dump(profiles, f)

# update requirements.txt with the dbt adapter depending on the type of datawarehouse
if dwh_type == 'postgres':
    with open('requirements.txt', 'a') as f:
        f.write("\ndbt-postgres==1.5.2")
elif dwh_type == 'snowflake':
    with open('requirements.txt', 'a') as f:
        f.write("\ndbt-snowflake==1.5.3")
elif dwh_type == 'redshift':
    with open('requirements.txt', 'a') as f:
        f.write("\ndbt-redshift==1.6.1")
elif dwh_type == 'bigquery':
    with open('requirements.txt', 'a') as f:
        f.write("\ndbt-bigquery==1.6.3")
