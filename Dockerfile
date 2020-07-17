FROM python:3.7
ENV HOME /root
WORKDIR $HOME

EXPOSE 8050

COPY ./app app

RUN pip install --trusted-host pypy.python.org -r app/requirements.txt

CMD [ "/bin/sh" , "-c" , "cd app/ && gunicorn --bind 0.0.0.0:8050 wsgi:application" ]
