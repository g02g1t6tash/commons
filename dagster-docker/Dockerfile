FROM python:3.9-slim

RUN pip install dagster dagit dagster-postgres

WORKDIR /opt/dagster/app

COPY . .

ENV DAGSTER_HOME=/opt/dagster/dagster_home

EXPOSE 3000

CMD ["dagit", "-h", "0.0.0.0", "-p", "3000"]
