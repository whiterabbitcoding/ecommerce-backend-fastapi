# pull official base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# set work directory
WORKDIR /usr/src/app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 80

# copy project
COPY . .

CMD ["./entrypoint.sh"]