FROM python:3.11-slim

LABEL org.opencontainers.image.description "Converts all OpenVAS xml files in /data to Excel"
LABEL org.opencontainers.image.source https://github.com/jemurai/openvasreporting

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && python ./setup.py install

VOLUME /data

CMD [ "./run.sh" ]
