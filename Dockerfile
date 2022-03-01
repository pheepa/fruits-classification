FROM python:3.6-slim
COPY ./app.py /deploy/
COPY ./requirements.txt /deploy/
COPY ./weights/weights_dense.wght /deploy/weights/
WORKDIR /deploy/
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "app.py"]