FROM python:3
MAINTAINER Your Name "griffin.ad.marketplace@gmail.com"
RUN mkdir -p /demo
COPY . /demo
RUN pip install -r /demo/requirements.txt
WORKDIR /demo
ENTRYPOINT ["python"]
CMD ["app.py"]

