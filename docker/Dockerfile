FROM alpine:3.17.3
EXPOSE 5000
WORKDIR /app
RUN apk add py3-flask
COPY ./app .
CMD ["flask", "run", "--host", "0.0.0.0"]
