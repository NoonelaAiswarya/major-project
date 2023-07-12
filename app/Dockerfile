FROM python:3.8-slim

# set the working directory inside the container
WORKDIR /app

# copy dependencies file

COPY  requirements.txt /app
# install the dependencies
RUN pip install -r requirements.txt

# copy the application code
COPY app.py /app

# expose the port on which the application would run
EXPOSE 5000

RUN groupadd -g 999 docker
RUN useradd -r -u 9999 -g docker aiswarya

# define the command to run the application
CMD ["python", "app.py"]
