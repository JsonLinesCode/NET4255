
FROM python:alpine3.23
WORKDIR /app
COPY . .
RUN apk update
RUN pip install -r requirements.txt

CMD ["python3", "-m", "flask", "--app", "hello", "run", "--debug", "--host=0.0.0.0", "--port=3000"]
EXPOSE 3000