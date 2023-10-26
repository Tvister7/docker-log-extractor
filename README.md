# docker-log-extractor

Run docker container by python script and send logs to ClowdWatch

## Requirements

- git
- poetry
- docker

## Installation

- `git clone https://github.com/Tvister7/docker-log-extractor.git && cd docker-log-extractor`
- `poetry install`

## Preparation

- Insert your <access_key_id> and <secret_access_key> to the `default_test.sh`
- Ensure `default_test.sh` has an execution right (do `chmod +x default_test.sh` if not)

## Usage

- `./default_test.sh`
