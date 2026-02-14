FROM python:3.12-slim

# working directory
WORKDIR /app

# copy .toml file to the container
COPY pyproject.toml .

COPY src src

# Now we have to install the dependencies from the toml file
RUN pip install --no-cache-dir .

# after the dependencies download copy rest of the files to container
CMD ["solr-sentinel"]
