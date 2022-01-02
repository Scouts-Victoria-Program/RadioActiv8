FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code

RUN apt-get update && \
    apt-get install -y \
      binutils \
      libproj-dev \
      gdal-bin \
      less vim \
    && \
    apt-get -y autoremove && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

HEALTHCHECK --interval=30s --retries=5 CMD ./healthcheck
ENTRYPOINT ["/code/docker-entrypoint.sh"]
