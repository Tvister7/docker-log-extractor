from logging import Formatter, Logger
from typing import Iterator

from cloudwatch.cloudwatch import CloudwatchHandler
from docker import from_env
from docker.errors import APIError, ContainerError, ImageNotFound
from docker.models.containers import Container
from logger import get_formatter, get_logger


def main(
    docker_image: str = "",
    bash_command: str = "",
    aws_cloudwatch_group: str = "",
    aws_cloudwatch_stream: str = "",
    aws_access_key_id: str = "",
    aws_secret_access_key: str = "",
    aws_region: str = "",
):
    try:
        print("Stage 1")
        bash_command = f'/bin/sh -c "{bash_command}"'

        print(
            docker_image,
            bash_command,
            aws_cloudwatch_group,
            aws_cloudwatch_stream,
            aws_access_key_id,
            aws_secret_access_key,
            aws_region,
            sep="\n\n",
        )
    except KeyboardInterrupt:
        print("Catch startup keyboard error")
        exit(1)

    try:
        print("Stage 2")
        container = create_container(docker_image, bash_command)
    except (ImageNotFound, APIError) as docker_error:
        print(f"Error with docker sdk {str(docker_error)}")
    except KeyboardInterrupt:
        print("Catch while container created error")
        exit(1)

    try:
        print("Stage 3")
        logger = get_logger()
        formatter = get_formatter()
        handler = CloudwatchHandler(
            log_group=aws_cloudwatch_group,
            log_stream=aws_cloudwatch_stream,
            access_id=aws_access_key_id,
            access_key=aws_secret_access_key,
            region=aws_region,
            overflow="split",
        )

        logger = configure_cloudwatch_logger(logger, formatter, handler)

        handle_log_stream(container.logs(stream=True), logger)

    except ContainerError as container_error:
        print(f"Error with docker container {str(container_error)}")
    except KeyboardInterrupt:
        print("Catch while container running error")
        container.kill()
    finally:
        container.remove(force=True)
        exit(1)


def configure_cloudwatch_logger(
    logger: Logger, formatter: Formatter, handler: CloudwatchHandler
) -> Logger:
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def handle_log_stream(stream: Iterator[bytes], logger: Logger) -> None:
    for log in stream:
        str_log = log.decode()
        # print(str_log)
        if str_log.startswith("ERROR"):
            logger.error(str_log)
        elif str_log.startswith("WARNING"):
            logger.warning(str_log)
        elif str_log.startswith("INFO"):
            logger.info(str_log)
        elif str_log.startswith("DEBUG"):
            logger.debug(str_log)
        else:
            logger.info(str_log)


def create_container(docker_image: str, bash_command: str) -> Container:
    client = from_env()
    return client.containers.run(docker_image, bash_command, detach=True)
