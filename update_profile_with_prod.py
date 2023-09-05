import sys
import yaml

# Load the profiles.yml file
with open('project_goes_here/profiles.yml', 'r') as f:
    profiles = yaml.safe_load(f)

# get the profile name from dbt_project.yml
with open('project_goes_here/dbt_project.yml', 'r') as f:
    dbt_project = yaml.safe_load(f)
    profile_name = dbt_project['profile']

# Get the type of datawarehouse we are using
dwh_type = sys.argv[1]
print("dwh_type: ", dwh_type)

# Add a new target called "prod" based on the type of datawarehouse
if dwh_type == 'postgres':
    profiles[profile_name]['outputs']['prod'] = {
        'type': 'postgres',
        'host': '{{ env_var("HOST") }}',
        'user': '{{ env_var("PROD_USERNAME") }}',
        'password': '{{ env_var("PROD_PASSWORD") }}',
        'port': '{{ env_var("PORT") | int }}',
        'dbname': '{{ env_var("DATABASE_NAME") }}',
        'schema': '{{ env_var("PROD_SCHEMA") }}',
        'threads': 8
    }
elif dwh_type == 'snowflake':
    profiles[profile_name]['outputs']['prod'] = {
        'type': 'snowflake',
        'account': '{{ env_var("SNOWFLAKE_ACCOUNT") }}',
        'role': '{{ env_var("SNOWFLAKE_ROLE") }}',
        'user': '{{ env_var("PROD_USERNAME") }}',
        'password': '{{ env_var("PROD_PASSWORD") }}',
        'database': '{{ env_var("DATABASE_NAME") }}',
        'schema': '{{ env_var("PROD_SCHEMA") }}',
        'warehouse': '{{ env_var("PROD_WAREHOUSE") }}',
        'threads': 8
    }
elif dwh_type == 'redshift':
    profiles[profile_name]['outputs']['prod'] = {
        'type': 'redshift',
        'host': '{{ env_var("HOST") }}',
        'user': '{{ env_var("PROD_USERNAME") }}',
        'password': '{{ env_var("PROD_PASSWORD") }}',
        'port': '{{ env_var("PORT") | int }}',
        'dbname': '{{ env_var("DATABASE_NAME") }}',
        'schema': '{{ env_var("PROD_SCHEMA") }}',
        'threads': 8
    }
elif dwh_type == 'bigquery':
    profiles[profile_name]['outputs']['prod'] = {
        'type': 'bigquery',
        'method': 'oauth',
        'project': '{{ env_var("PROJECT_NAME") }}',
        'dataset': '{{ env_var("PROD_DATASET") }}',
        'threads': 8
}

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

