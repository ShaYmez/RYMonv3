FROM python:3.11-slim-bookworm

WORKDIR /monitor

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev libssl-dev gosu \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc \
    && rm -rf /var/lib/apt/lists/*

COPY monitor.py config.py mon_db.py rymon_SAMPLE.cfg ./
COPY templates/ templates/
COPY data/ data/
COPY entrypoint /entrypoint
RUN sed -i 's/\r$//' /entrypoint \
    && chmod +x /entrypoint \
    && mkdir -p log \
    && useradd -r -u 54000 -d /monitor -s /usr/sbin/nologin radio \
    && chown -R radio:radio /monitor

EXPOSE 9000

ENTRYPOINT ["/entrypoint"]
