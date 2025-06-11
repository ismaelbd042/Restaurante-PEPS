FROM python:3.8.18
RUN mkdir /app
WORKDIR /app
ADD ./python .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py", "runserver"]
