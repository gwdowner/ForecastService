FROM python:3.7.6
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
ENV PORT=8080
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["server.py"]
