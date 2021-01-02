FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

COPY server.py .
CMD ["python3", "server.py"]