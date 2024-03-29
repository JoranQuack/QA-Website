# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install -U prisma

LABEL io.portainer.accesscontrol.users=joran

COPY . .

RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

RUN npm install
RUN npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css

RUN python3 -m prisma db push

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
