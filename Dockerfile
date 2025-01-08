# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY Flaskapi.py /app/Flaskapi.py

COPY requirements.txt /app/requirements.txt

COPY dataIngestion.py /app/dataIngestion.py

RUN pip3 install -r requirements.txt

EXPOSE 5000

# ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

CMD ["python", "Flaskapi.py"]
