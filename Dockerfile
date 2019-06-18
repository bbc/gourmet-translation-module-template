FROM python:3

WORKDIR /app

COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 4000 available
EXPOSE 4000

# Run app.py when the container launches
CMD ["python", "app.py"]
