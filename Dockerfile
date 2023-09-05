###############################################################################
#   Copyright (C) 2020 Shane aka, ShaYmez <support@gb7nr.co.uk>  
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
###############################################################################

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
