
# use after building base image from /docker-setup/Dockerfile
# to update source files and initial exec script

# here use the name of the base image
FROM metamap-python-java:latest

WORKDIR /mm_app/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY mm_server.py .
COPY setup.sh .

RUN tr -d "\r" < setup.sh > start.sh

CMD sh start.sh

# chd to dockerfile dir and build the image with:
# > docker build -t metamap-server:latest .

# then, run the container using the image:
# > docker run --publish 7777:7777 --detach --name metamap metamap-server:latest