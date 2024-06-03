# pull official base image
FROM public.ecr.aws/docker/library/python:3.9

# RUN apt-get update \
#     && apt-get -y install libpq-dev gcc \
#     && pip install psycopg2 gunicorn

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

# Install aws cli
RUN apt-get update
RUN apt-get install -y \
        python3 \
        python3-pip \
        python3-setuptools \
        groff \
        less \
    && pip3 install --upgrade pip \
    && apt-get clean

RUN pip3 --no-cache-dir install --upgrade awscli

# set work directory
WORKDIR /usr/src/app

# setup git access to AWS CodeCommit
# RUN aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
# RUN aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
# RUN git config --global credential.helper '!aws codecommit credential-helper $@'
# RUN git config --global credential.UseHttpPath true

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev
# /usr/src/app/bastion-host.pem
# COPY bastion-host.pem ./
# RUN chmod 400 bastion-host.pem
# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
# RUN pip install fcm-django
# RUN pip install celery
# RUN pip install openpyxl

# CMD celery -A WorkLog worker -l info


# copy entrypoint.sh
COPY entrypoint.sh ./
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh

# copy project
COPY . .



EXPOSE 80

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]