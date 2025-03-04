FROM jupyter/scipy-notebook:latest

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY data /home/jovyan/data/

CMD ["start-notebook.py", "--NotebookApp.token=''"]