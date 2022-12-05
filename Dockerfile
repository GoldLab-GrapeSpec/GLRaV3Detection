FROM python:3.7

WORKDIR /app

COPY requirements.txt ../tmp/requirements.txt

RUN pip install -r ../tmp/requirements.txt

# No need for this directory anymore
RUN rm -r ../tmp/

COPY ./data_management_python/ /app/data_management_python/

WORKDIR /app/data_management_python/

# Install package for local editing
RUN pip install -e .

WORKDIR /app/data_management_python/dairymgr/

CMD ["python", "-u", "python_server.py", "-r", "both", "-p", "8000", "-s", "serversnapshot.txt"]
