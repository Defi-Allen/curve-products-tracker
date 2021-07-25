FROM python:3

COPY requirements.txt /app/
RUN apt update && apt upgrade -y && \
    pip3 install -r /app/requirements.txt

COPY src/ /app/src/
COPY main.py /app/

CMD ["python3", "-u", "/app/main.py"]
