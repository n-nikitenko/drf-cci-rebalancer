FROM python:3.8.10-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VENV="/opt/poetry-venv" \
    POETRY_CACHE_DIR="/opt/.cache" \
    PATH="${POETRY_VENV}/bin:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /code
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

FROM python:3.8.10-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-config.settings}

ENV PATH="/opt/poetry-venv/bin:$PATH"


# Копируем только необходимые файлы из этапа сборки
COPY --from=builder /opt/poetry-venv /opt/poetry-venv
COPY --from=builder /code .

WORKDIR /code
COPY . .

RUN poetry install --no-interaction --no-ansi