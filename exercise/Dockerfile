#########################
# Enter your code below #
#########################
FROM python:3.8.5-alpine3.12
WORKDIR /usr/app
RUN pwd
COPY . .
RUN pip install -r requirements.txt
RUN export FLASK_ENV=development
EXPOSE 5000


CMD ["flask", "run", "--host=0.0.0.0"]