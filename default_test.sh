#! /bin/zsh

poetry run python src --docker-image python \
 --bash-command $'pip install pip -U && \
pip install tqdm && \
python -c \'
import time
counter = 0
while True:
    print(counter)
    counter = counter + 1
    time.sleep(0.1)
\'' \
 --aws-cloudwatch-group test-task-group-1 --aws-cloudwatch-stream test-task-stream-1 \
 --aws-access-key-id <access_key_id> --aws-secret-access-key <secret_access_key> \
 --aws-region us-east-1