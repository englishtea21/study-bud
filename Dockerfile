FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
# requirements.txt - зависимости django проекта
RUN pip install -r requirements.txt