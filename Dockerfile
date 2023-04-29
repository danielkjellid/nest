FROM node:lts-alpine as nest-frontend

RUN mkdir /app
WORKDIR /app

# Required system packages
RUN apk add --update --no-cache git

COPY .nvmrc package.json package-lock.json /app/
RUN npm ci

# Copy application files
COPY tsconfig.json tsconfig.node.json vite.config.ts schema.json /app/
COPY frontend /app/frontend/

RUN npm run build:production

# ----------------------------------------------------------

FROM python:3.11.1 as nest

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH /app/

# Add app user
RUN groupadd -r nest && useradd --create-home nest -g nest

# Get postgresql-14 package manually, as the official package version only supports
# postgresql-13. These three lines can be removed once the official package is updated.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y lsb-release
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    bash-completion \
    less \
    lsof \
    vim \
    curl \
    postgresql-14 \
    awscli \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache poetry==1.3.2

# Create app directory and required subdirectories
RUN mkdir -p /app/public /app/vite_output
RUN chown -R nest:nest /app

# Set app user and working directory
USER nest
WORKDIR /app

COPY --chown=nest poetry.lock pyproject.toml poetry.toml manage.py .env.test /app/
RUN poetry install --no-root --only main --no-interaction --no-ansi

# Render needs a .ssh folder to make ssh tunneling work.
RUN mkdir ./.ssh && chmod 700 ./.ssh

# Copy application files
COPY --chown=nest nest/ /app/nest/
COPY --chown=nest cli/ /app/cli/

COPY --chown=nest --from=nest-frontend /app/static/vite_output/ /app/static/

# Collect static files and migrate
#RUN poetry run python manage.py collectstatic --noinput
#RUN poetry run python manage.py migrate

ENV DJANGO_VITE_DEV_MODE=False

COPY --chown=nest docker-entrypoint.sh /app

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]