FROM python:3.6

WORKDIR /usr/app

# Install Java
RUN echo 'deb http://cdn-fastly.deb.debian.org/debian  stretch main contrib non-free' > /etc/apt/sources.list.d/jessie-backports.list && \
    apt-get -y update && \
    apt-get install --no-install-recommends -y openjdk-8-jre-headless ca-certificates-java && \
    rm /etc/apt/sources.list.d/jessie-backports.list && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD ./requirements.txt ./
RUN pip install -r requirements.txt
ADD ./ ./


CMD ["python3", "app.py"]
