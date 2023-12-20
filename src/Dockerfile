FROM python:3.9

COPY ./ /ansible_runner/

WORKDIR /ansible_runner

RUN python3 -m pip install --upgrade pip && python3 -m pip install -e .

CMD python3 -m uvicorn ansible_runner:app --host 0.0.0.0 --port $ANSIBLE_RUNNER_INNER_PORT
