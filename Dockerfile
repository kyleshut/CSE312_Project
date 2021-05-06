FROM python:3.8

# Set the home directory to /root
ENV HOME /root

# cd into the home directory
WORKDIR /root

# Copy all app files into the image
COPY . .

# Download dependancies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Allow port 8000 to be accessed
# from outside the container
EXPOSE 8000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

# Run the app
CMD /wait && python3 server.py