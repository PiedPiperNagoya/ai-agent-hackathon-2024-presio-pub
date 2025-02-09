FROM python:3.12

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
        gnupg \
        chromium \
        fonts-ipafont-gothic \
        fonts-ipafont-mincho \
        ffmpeg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g @marp-team/marp-cli && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED True
ENV TMPDIR=/tmp

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --upgrade --no-cache-dir -r requirements.txt

ENV APP_HOME /app
COPY . ${APP_HOME}
WORKDIR ${APP_HOME}

ENV PORT 7860
EXPOSE ${PORT}

CMD ["python", "app.py"]
