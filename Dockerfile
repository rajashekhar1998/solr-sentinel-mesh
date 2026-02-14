FROM python:3.14-slim

# working directory
WORKDIR /app

# copy .toml file to the container
COPY pyproject.toml .

# Now we have to install the dependencies from the toml file
RUN pip install --upgrade pip && \
    pip install --no-cache-dir .

# after the dependencies download copy rest of the files to container
COPY . .
