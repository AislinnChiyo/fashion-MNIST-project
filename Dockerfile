 
# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install tensorflow  -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt #  -i https://pypi.tuna.tsinghua.edu.cn/simple 
RUN apt update
RUN apt install -y libgl1-mesa-dev libgtk2.0-dev


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME fashion-MNIST-Project

# Run app.py when the container launches
CMD ["python", "upload_pictures.py"]
