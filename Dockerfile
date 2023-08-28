FROM python:alpine3.17

COPY entrypoint /entrypoint

RUN adduser -D -u 54000 radio
RUN	apk update && \
	apk add git gcc musl-dev libffi-dev openssl-dev cargo && \
    pip install --upgrade pip && \
    pip cache purge && \
	git clone https://github.com/shaymez/RYMonv3.git /monitor && \
    cd /monitor && \
	pip install --no-cache-dir -r requirements.txt && \
	apk del git gcc musl-dev && \
	chown -R radio /monitor

USER radio

ENTRYPOINT [ "/entrypoint" ]