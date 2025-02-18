FROM jupyter/scipy-notebook:latest

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY data/air-sensor-data.txt /home/jovyan/data/air-sensor-data.txt

CMD ["start-notebook.py", "--NotebookApp.token=''"]