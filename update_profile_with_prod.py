import yaml

# Load the profiles.yml file
with open('project_goes_here/profiles.yml', 'r') as f:
    profiles = yaml.safe_load(f)

# Add a new target called "prod"
profiles['dbt_project']['outputs']['prod'] = {
    'type': 'postgres',
    'host': '{{ env_var("HOST") }}',
    'user': '{{ env_var("PROD_USERNAME") }}',
    'password': '{{ env_var("PROD_PASSWORD") }}',
    'port': '{{ env_var("PORT") }}',
    'dbname': '{{ env_var("DATABASE_NAME") }}',
    'schema': '{{ env_var("PROD_SCHEMA") }}',
    'threads': 8
}

# Save the updated profiles.yml file
with open('project_goes_here/profiles.yml', 'w') as f:
    yaml.dump(profiles, f)