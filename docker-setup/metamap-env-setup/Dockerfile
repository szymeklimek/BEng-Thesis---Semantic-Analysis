
# dockerfile for building a
# jdk1.8-python3.6.6 base image
# with libraries and metamap unpacked and ready to install

FROM rappdw/docker-java-python:openjdk1.8.0_171-python3.6.6

WORKDIR /mm_app/

ADD public_mm_linux_main_2020.tar.bz2 .
ENV PATH=mm_app/public_mm/bin:${PATH}

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN git clone https://github.com/AnthonyMRios/pymetamap.git
RUN cd pymetamap && python setup.py install

# chd to dockerfile dir and build the image with:
# > docker build -t metamap-python-java:latest .
# (do not forget the dot!)