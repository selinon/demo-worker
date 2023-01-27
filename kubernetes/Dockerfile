FROM quay.io/fedora/python-39

ENV PYTHONPATH=.
WORKDIR /app/

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY app.py entrypoint.py /app/
COPY demo_worker /app/demo_worker

ENTRYPOINT ["python3", "app.py"]
