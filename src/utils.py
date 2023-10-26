from boto3 import client


def check_logs(
    aws_cloudwatch_group: str = "",
    aws_cloudwatch_stream: str = "",
    aws_access_key_id: str = "",
    aws_secret_access_key: str = "",
    aws_region: str = "",
) -> None:
    response = client(
        "logs",
        region_name=aws_region,
        aws_secret_access_key=aws_secret_access_key,
        aws_access_key_id=aws_access_key_id,
    ).filter_log_events(
        logGroupName=aws_cloudwatch_group,
        logStreamNames=[
            aws_cloudwatch_stream,
        ],
        limit=123,
        interleaved=True | False,
    )

    print(response)
