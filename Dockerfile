FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
COPY ./src .
#CMD ["uvicorn", "main:app", "--reload"]
CMD ["python", "main.py"]