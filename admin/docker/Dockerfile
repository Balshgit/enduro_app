ARG PYTHON_VERSION=3.14.1
ARG UV_VERSION=0.9.15

# Interpolation is not supported in COPY --from commands
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS dependency_resolver

# Relies on base python image to be based on bookworm slim.
# May require update if production image base changes.
FROM python:${PYTHON_VERSION} AS builder
COPY --from=dependency_resolver /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 PYTHONUNBUFFERED=1


WORKDIR /app/
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync


FROM python:${PYTHON_VERSION} AS production
WORKDIR /app/
# It is important to use the image that matches the builder, as the path to the
# Python executable must be the same, e.g., using `python:3.11-slim-bookworm`
# will fail.

# create user enduro
RUN mkdir /home/enduro \
      && groupadd -r enduro && useradd -d /home/enduro -r -g enduro enduro \
      && chown enduro:enduro -R /home/enduro

# Copy the application from the builder
COPY --from=builder --chown=enduro:enduro /app/ /app
COPY . .

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
RUN chmod +x /app/docker/docker-entrypoint.sh

USER enduro

EXPOSE 8080
WORKDIR /app/app/

ENTRYPOINT ["/app/docker/docker-entrypoint.sh"]
CMD ["help"]