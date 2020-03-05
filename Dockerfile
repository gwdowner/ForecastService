FROM python:3.7.6
WORKDIR /usr/src/app
RUN ls
COPY . .
#RUN pip install -r requirements.txt
RUN ls -r
ENTRYPOINT ["python"]
CMD ["server.py"]