FROM python:3.7

WORKDIR /project

ADD . /project
RUN pip install -r requirement.txt

EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0"]

