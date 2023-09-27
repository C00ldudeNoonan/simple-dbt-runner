-- Execute with: dbt run-operation drop_old_relations --args '{"dry_run": True}'
-- to run the delete, run w/o the args
-- this simplified version simply drops schemas that start with PR

{% macro drop_old_relations(dry_run='false') %}
{% set cleanup_query %}
      with models_to_drop as (
        select
            distinct table_schema
        from 
          {{ target.database }}.information_schema.tables
        where table_schema like 'PR%'
      )
      select 
        CONCAT( 'drop schema "' , table_schema , '" cascade;' ) as drop_commands
      from 
        models_to_drop
      order by drop_commands desc
  {% endset %}
{% do log(cleanup_query, info=True) %}
{% set drop_commands = run_query(cleanup_query).columns[0].values() %}
{% if drop_commands %}
  {% for drop_command in drop_commands %}
    {% do log(drop_command, True) %}
    {% if dry_run == 'false' %}
      {% do run_query(drop_command) %}
    {% endif %}
  {% endfor %}
{% else %}
  {% do log('No relations to clean.', True) %}
{% endif %}
{%- endmacro -%}