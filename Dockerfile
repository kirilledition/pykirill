# Use an official Python runtime as a parent image
FROM python:3.12.4-alpine3.20

# Metadata as labels
LABEL maintainer="Kirill Denisov <kirill.denisov@gero.ai>"
LABEL description="A Docker image for the pykirill package."
LABEL license="MIT"

# Set the working directory in the container
WORKDIR /app

# Copy the package wheel file into the container
COPY dist /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    apk add py3-scikit-learn && \
    pip install *.whl

# Command to run your package
CMD ["pykirill"]