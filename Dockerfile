FROM python:3

WORKDIR /opt/finances

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./


ENV FLASK_APP=test.py
ENV FLASK_ENV=development
EXPOSE 5000
CMD [ "python", "run.py" ]
