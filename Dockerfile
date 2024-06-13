FROM python:3.12

WORKDIR app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "challenge/challenge_python.py"]
