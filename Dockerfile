FROM python:3.7.6
COPY . /usr/src
WORKDIR /usr/src
RUN pip install -r requirements.txt
RUN ls
RUN tree
ENTRYPOINT ["python"]
CMD ["server.py"]