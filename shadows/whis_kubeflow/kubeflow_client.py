from kfp import Client


def submit_pipeline(pipeline_func, arguments: dict):
    client = Client()
    run = client.create_run_from_pipeline_func(
        pipeline_func=pipeline_func, arguments=arguments
    )
    return run.run_id
