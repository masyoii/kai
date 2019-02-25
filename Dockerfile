FROM python:3
ADD kai_backd4.py /app/kai_backd4.py
RUN pip install schedule
RUN pip install pycurl
CMD [ "python", "/app/kai_backd4.py" ]