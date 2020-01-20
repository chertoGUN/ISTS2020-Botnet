FROM python:alpine

COPY requirements.txt /tmp/requirements
RUN pip3 install -r /tmp/requirements

COPY . /opt/botnet
 
WORKDIR /opt/botnet

CMD ["python3", "/opt/botnet/server.py"]