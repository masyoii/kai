FROM python:2.7.14

RUN mkdir -p /app /data
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "kai_backd.py" ]
