FROM python:3.11

WORKDIR ./blogapi

COPY ./requirements.txt /blogapi/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /blogapi/requirements.txt

COPY ./app /blogapi/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]