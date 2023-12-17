FROM python:3.10

ENV DASH_DEBUG_MODE False
COPY ./application /application
WORKDIR /application
RUN apt-get update
RUN apt-get install
RUN pip install -r requirements.txt
RUN apt-get install gunicorn -y
EXPOSE 8080
CMD ["gunicorn", "index:server", "-b", "0.0.0.0:8080", "--workers=5"]
#ENTRYPOINT ["tail"] CMD ["-f","/dev/null"]