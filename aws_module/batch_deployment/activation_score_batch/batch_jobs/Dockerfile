FROM python:3.8-slim-buster

RUN mkdir /data
RUN pip install boto3 && pip install pandas && pip install numpy

COPY get_zscore.py .

CMD ["python", "get_zscore.py"]