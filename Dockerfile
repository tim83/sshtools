LABEL authors="Tim Mees"
ARG PYTHON_IMAGE_TAG=3.10

FROM python:${PYTHON_IMAGE_TAG} AS python-base
FROM python-base AS builder

# default is the latest version
ARG POETRY_VERSION=""

ENV POETRY_VERSION=${POETRY_VERSION}
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
# Location for the venv and the project config files
ENV PYSETUP_PATH="/opt/pysetup"

ENV PATH="$POETRY_HOME/bin:$PATH"

# Installs POETRY_VERSION in POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR ${PYSETUP_PATH}
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-dev

FROM python-base as development

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
RUN poetry install

# Mount source to /app for development
WORKDIR /app
COPY . /app

FROM python-base as production

COPY --from=builder $POETRY_HOME $POETRY_HOME

WORKDIR /app
COPY . /app
