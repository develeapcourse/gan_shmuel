# Use an official Python runtime as an image
FROM python:3.6

# The EXPOSE instruction indicates the ports on which a container # # will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000

# Install any needed packages specified in requirements.txt
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

# Run app.py when the container launches
RUN mkdir /in /app
COPY in/ /in
COPY .env /app
COPY app.py /app
COPY mySQL_DAL.py /app
CMD python3 /app/app.py
