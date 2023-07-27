FROM python:3.8-slim

ENV WORKDIR /opt/app
WORKDIR ${WORKDIR}
ENV PYTHONPATH=${PYTHONPATH}:${WORKDIR}

RUN apt update

COPY . .

RUN pip install -Ur requirements.txt

CMD ["uvicorn", "api.main:api", "--host", "0.0.0.0", "--port", "8080"]
