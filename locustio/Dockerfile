FROM python:3.7-alpine

WORKDIR /locust

RUN apk --no-cache add g++ zeromq-dev libffi-dev && rm -rf /var/cache/apk/*

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8089
ENTRYPOINT ["locust", "-f", "locustfile.py"]