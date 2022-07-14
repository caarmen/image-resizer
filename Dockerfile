FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get --assume-yes install cron

COPY requirements/prod.txt requirements.txt

RUN pip install -r requirements.txt

COPY imageresizer imageresizer

CMD cron_comment="purge imageresizer cache" ;\
    cron_command="cd /app && LOG_FOLDER=${LOG_FOLDER:-.} CACHE_VALIDITY_S=${CACHE_VALIDITY_S:-86400} /usr/local/bin/python -m imageresizer.purge" ; \
    cron_schedule=${CRON_SCHEDULE:-"20 2 * * *"}; \
    (crontab -l |grep --invert-match --fixed-strings  "$cron_comment"; echo "$cron_schedule $cron_command #$cron_comment")  | crontab -  && \
    cron && \
    CACHE_DIR=/var/cache/image-resizer python -m imageresizer.main
