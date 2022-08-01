FROM python:3.8.6-slim-buster
RUN mkdir /opt/quantum_bootcamp
WORKDIR /opt/quantum_bootcamp
COPY requirements.txt /opt/quantum_bootcamp/
RUN python3 -m pip install --no-cache-dir -r /opt/quantum_bootcamp/requirements.txt
