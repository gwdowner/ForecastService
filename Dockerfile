FROM python:3.7.6
COPY . /www
WORKDIR /www
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["server.py"]