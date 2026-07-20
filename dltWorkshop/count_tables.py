### with relation to Q2. How many tables did dlt create in the agent_traces schema?

import dlt

pipeline = dlt.pipeline(
    pipeline_name="logfire_pipeline",
    destination="duckdb",
    dataset_name="logfire_data",
)

with pipeline.sql_client() as client:
    result = client.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'logfire_data'"
    )
    count = result.fetchone()[0]
    print(f"Number of tables in 'agent_traces' schema: {count}")
