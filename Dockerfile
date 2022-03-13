FROM 6pxgqc5k.mirror.aliyuncs.com/library/debian:10.9
LABEL maintainer="tangdyy@qq.com"
LABEL description = "onlyuserclient"
COPY ./demo  /opt/demo
COPY ./requirements.txt  /opt/demo/requirements.txt
COPY ./builds/debian/sources.list.buster /etc/apt/sources.list
RUN apt-get update -y \ 
    && apt-get install -y \
       python3-dev \
       default-libmysqlclient-dev \
       build-essential \
       python3-pip \ 
    && apt-get clean \
    && chmod -R a+x /opt/demo/bin \
    && pip3 install --no-cache-dir onlyuserclient==1.0.10 \
    && pip3 install --no-cache-dir --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/ \
       -r /opt/demo/requirements.txt 
ENV UWSGI_LISTEN_PORT="8080" \
    DJANGO_PROJECT_DIR="/opt/demo/billing" \
    DJANGO_PROJECT_WSGI_MODULE="billing.wsgi" \
    DJANGO_PROJECT_SETTINGS="billing.settings" \
    DJANGO_SETTINGS_MODULE="billing.settings" \
    UWSGI_PROCESSES="4" \
    UWSGI_THREADS="20" 

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "-c", "/opt/wellbill/bin/entrypoint.sh"]
