FROM python:3-alpine
RUN pip install paho-mqtt flask flask_restful flask_pymongo requests
ADD ./mqtt/ /mqtt/
ADD ./rest_api/api.py /rest_api/api.py
CMD /usr/local/bin/python /rest_api/api.py
