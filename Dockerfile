FROM python:3.6-slim
ADD ./app /deploy/
COPY ./requirements.txt /deploy/
COPY ./configs/class2name.json /deploy/configs/
WORKDIR /deploy/
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "app.py"]