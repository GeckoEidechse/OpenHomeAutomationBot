FROM python:3.11

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
# README is needed for some reason?
COPY README.md /app/
COPY openhomeautomationbot/* /app/openhomeautomationbot/
COPY scripts/* /app/scripts

RUN pip install poetry
RUN poetry install --no-interaction --no-ansi

CMD ["bash", "scripts/infinite-run.sh"]
