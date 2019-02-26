FROM python:3

RUN mkdir -p /app /data
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "kai_backd4.py" ]
