
FROM python:3.9

RUN mkdir -p /home/app
COPY . /home/app
COPY requirements.txt .

# Copy the Python script to the container
COPY .env .
COPY match.py .
COPY get_data.py .
# Install dependencies
RUN pip install  --no-cache-dir -r requirements.txt

# Set the entry point command
CMD ["python", "match.py"]
