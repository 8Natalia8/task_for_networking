FROM python:3.8.5
LABEL maintainer="navsta99@gmail.com"
WORKDIR /data
RUN pip install scapy
ADD main.py .
CMD ["python","./main.py"]

