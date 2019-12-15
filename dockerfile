FROM tiangolo/uwsgi-nginx-flask:python3.6

# Install packages
RUN pip install Flask-RESTful==0.3.7
RUN pip install mysql-connector-python==8.0.15
RUN pip install requests==2.22.0
RUN pip install redis==3.3.11

COPY ./app /app
