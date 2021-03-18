FROM python:3.9

WORKDIR /app

RUN pip install poetry==1.1.5

COPY pyproject.toml poetry.lock /app/

# use poetry to emit the dependencies but use pip to install without a virtualenv
# doing this because Docker is already a contained environment so virtualenv seems unnecessary
RUN poetry export --without-hashes -f requirements.txt | pip install -r /dev/stdin

COPY example /app

ENV FLASK_ENV=development
ENV FLASK_APP=main
EXPOSE 5000

RUN chmod u+x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]