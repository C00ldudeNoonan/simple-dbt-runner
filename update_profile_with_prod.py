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

# Add a new target called "prod"
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

# Save the updated profiles.yml file
with open('project_goes_here/profiles.yml', 'w') as f:
    yaml.dump(profiles, f)

print(profiles)