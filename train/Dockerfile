FROM tensorflow/tensorflow:latest-gpu

COPY train.py .

# Add deadsnakes repo
RUN apt update
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y

# Install Python 3.10
RUN apt update && apt install -y python3.10 python3.10-distutils
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

RUN apt-get install git -y
RUN pip install git+https://github.com/keras-team/keras-nlp.git -q

# Replace python shell with python3.10
RUN unlink /usr/bin/python
RUN ln -s /usr/bin/python3.10 /usr/bin/python

RUN pip install boto3

CMD python train.py
