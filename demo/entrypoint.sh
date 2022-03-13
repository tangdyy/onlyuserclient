#!/bin/bash
work_path=$(dirname $(readlink -f $0))
cd ${work_path}

if [ 0"$UWSGI_LISTEN_PORT" = "0" ]; then
   UWSGI_LISTEN_PORT="8080"
fi

if [ 0"$UWSGI_PROCESSES" = "0" ]; then
   UWSGI_PROCESSES="4"
fi

if [ 0"$UWSGI_THREADS" = "0" ]; then
   UWSGI_THREADS="20"
fi

uwsgi --http 0.0.0.0:${UWSGI_LISTEN_PORT} \
      --chdir "/opt/demo/billing" \
      --module "billing.wsgi" \
      --env DJANGO_SETTINGS_MODULE="billing.settings" \
      --master \
      --processes ${UWSGI_PROCESSES} \
      --threads ${UWSGI_THREADS} \
      --uid=1000  \
      --gid=2000  \
      --enable-threads 