#"""Project {project_name}
#Author  {author}
#email   {author_email}
#"""

# Set image labels
LABEL project.name="{project_name}"
LABEL project.version="{project_version_major}.{project_version_minor}"
LABEL project.author="{author}"
LABEL project.author.email="{author_email}"


# Set python base image
FROM python:3-stretch

# Set the working directory
WORKDIR /usr/src/app

# Copy files
COPY . {project_root}/

# Install  internal requirements
RUN pip install --no-cache-dir  {project_root}/

# Define command to execute
ENV TERM xterm
ENTRYPOINT ["{project_root}"]