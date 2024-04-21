FROM tiangolo/meinheld-gunicorn-flask:latest

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

CMD ["gunicorn", "--bind", "0.0.0.0:80", "wsgi:app"]
