#FROM python:3
FROM frolvlad/alpine-python-machinelearning
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5101
CMD ["python", "predictor.py"]