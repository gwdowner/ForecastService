FROM python:3.7.6
WORKDIR /usr/src/app
RUN ls
COPY . .
RUN pip install -r requirements.txt
RUN ls -r
ENV PORT=8080
ENTRYPOINT ["python"]
CMD ["server.py"]
EXPOSE 8080