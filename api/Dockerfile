FROM python:3.9

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r ./requirements.txt

WORKDIR /app

COPY ./ /app

ENTRYPOINT ["python"]

CMD ["main.py"]

EXPOSE 5000
