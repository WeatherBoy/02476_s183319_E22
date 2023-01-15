# Base image
FROM python:3.7-slim

# install python
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/

# Copying some things (we didn't wanna copy a lot as we wanted our image)
# to be as small as possible
COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY src/ src/
COPY data/ data/

# Setting working directory and install the requirements file
WORKDIR /
RUN pip install -r requirements.txt --no-cache-dir

# Setting the entrypoint to be the train_model.py 
ENTRYPOINT ["python", "-u", "src/models/train_model.py"]
