#parse('bash_header')

# Set image labels
LABEL project.name="${PROJECT_NAME}"
LABEL project.version="${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}"
LABEL project.author="${AUTHOR}"
LABEL project.author.email="${AUTHOR_EMAIL}"
LABEL project.creation="${DAY}-${MONTH}-${YEAR}"

# Set python base image
FROM python:3-stretch

# Set the working directory
WORKDIR /usr/src/app

# Copy files
COPY . app/

# Install  internal requirements
RUN pip install --no-cache-dir  app/

# Define command to execute
ENV TERM xterm
ENTRYPOINT ["{PROJECT_ENTRY_POINT}"]