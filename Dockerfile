# Python base image
FROM python:3.12.3

# info
LABEL version='0.01'
LABEL mantainer='jenius-group'

# working directory
WORKDIR /app

COPY . /app

# dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose ports 
EXPOSE 8981

# entry point
ENTRYPOINT ["python", "main.py"]
CMD ["--host", "0.0.0.0", "--port", "8981", "--transport", "stdio"]