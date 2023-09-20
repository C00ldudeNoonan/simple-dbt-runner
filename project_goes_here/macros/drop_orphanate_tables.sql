{%- macro drop_orphanate_tables(dry_run='false') -%}

    {%- if execute -%}

        -- Create empty dictionary that will contain the hierarchy of the models in dbt
        {%- set current_model_locations = {} -%}

        -- Insert the hierarchy database.schema.table in the dictionary above
        {%- for node in graph.nodes.values() | selectattr("resource_type", "in", ["model", "seed", "snapshot"]) -%}

            {%- set database_name = node.database.upper() -%}
            {%- set schema_name = node.schema.upper() -%}
            {%- set table_name = node.alias if node.alias else node.name -%}

            -- Add db name if it does not exist in the dict
            {%- if not database_name in current_model_locations -%}
                {% do current_model_locations.update({database_name: {}}) -%}
            {%- endif -%}

            -- Add schema name if it does not exist in the dict
            {%- if not schema_name in current_model_locations[database_name] -%}
                {% do current_model_locations[database_name].update({schema_name: []}) -%}
            {%- endif -%}

            -- Add the tables for the db and schema selected
            {%- do current_model_locations[database_name][schema_name].append(table_name.upper()) -%}

        {%- endfor -%}

        {{ log(current_model_locations) }}

    {%- endif -%}

    -- Query to retrieve the models to drop
    {%- set cleanup_query -%}

        WITH models_to_drop AS (
            {%- for database in current_model_locations.keys() -%}

                SELECT
                    CASE
                        WHEN table_type = 'BASE TABLE' THEN 'TABLE'
                        WHEN table_type = 'VIEW' THEN 'VIEW'
                        ELSE NULL
                    END AS relation_type,
                    table_catalog,
                    table_schema,
                    table_name,
                    table_catalog || '.' || table_schema || '.' || table_name as relation_name
                FROM {{ database }}.information_schema.tables
                WHERE
                    LOWER(table_schema) IN ('{{ "', '".join(current_model_locations[database].keys())|lower }}')
                    AND NOT (
                        {%- for schema in current_model_locations[database].keys() -%}
                            LOWER(table_schema) = LOWER('{{ schema }}') AND LOWER(table_name) IN ('{{ "', '".join(current_model_locations[database][schema])|lower }}')
                            {% if not loop.last %} OR {% endif %}
                        {%- endfor %}
                    )

                {% if not loop.last -%} UNION ALL {%- endif %}
            {%- endfor -%}
        )
        -- Create the DROP statments to be executed in the database
        SELECT 'DROP ' || relation_type || ' IF EXISTS ' || table_catalog || '.' ||table_schema || '.' || table_name || ';' AS drop_commands
        FROM models_to_drop
        WHERE relation_type IS NOT NULL

    {%- endset -%}

    -- Execute the DROP statments above

    {%- set drop_commands = run_query(cleanup_query).columns[0].values() -%}

    {%- if drop_commands -%}

        {%- for drop_command in drop_commands -%}

            {%- do log(drop_command, True) -%}

            {%- if dry_run.upper() == 'FALSE' -%}
                {%- do run_query(drop_command) -%}
                {%- do log('Executed', True) -%}
            {%- endif -%}

        {%- endfor -%}

    {%- else -%}

        {%- do log('No relations to clean', True) -%}

    {%- endif -%}

{%- endmacro -%}
