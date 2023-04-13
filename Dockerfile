FROM alpine:3.17.3
WORKDIR /app
RUN apk add py3-pip
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./app .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
