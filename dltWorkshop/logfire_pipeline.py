import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources
from dlt.common.pendulum import pendulum


@dlt.source(name="logfire")
def logfire_source(access_token: str = dlt.secrets.value):
    """Load data from Pydantic Logfire Query API.

    Args:
        access_token: Logfire r+st token. Auto-loaded from secrets.toml.
    """
    seven_days_ago = pendulum.now("UTC").subtract(days=7).to_iso8601_string()

    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://logfire-eu.pydantic.dev/",
            "auth": {
                "type": "bearer",
                "token": access_token,
            },
        },
        "resources": [
            {
                "name": "logfire_records",
                "endpoint": {
                    "path": "v2/query",
                    "method": "POST",
                    "json": {
                        "sql": "SELECT * FROM records LIMIT 100",
                        "min_timestamp": seven_days_ago,
                    },
                    "data_selector": "data",
                    "headers": {
                        "Accept": "application/json",
                    },
                },
            },
        ],
    }

    yield from rest_api_resources(config)


def load_logfire() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="logfire_pipeline",
        destination="duckdb",
        dataset_name="logfire_data",
    )

    load_info = pipeline.run(logfire_source())
    print(load_info)


if __name__ == "__main__":
    load_logfire()
