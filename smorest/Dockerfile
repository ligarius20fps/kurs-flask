FROM alpine:3.17.3
EXPOSE 5000
WORKDIR /app
RUN apk add py3-pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app .
CMD ["flask", "run", "--host", "0.0.0.0"]
