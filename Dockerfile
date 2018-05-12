#!/usr/bin/env bash

# pymake
# -------------------------------
#  - Eugenio Marinetto
#  - nenetto@gmail.com
# -------------------------------
# Created 12-05-2018

## Base image
FROM python:3.6.5-stretch

# Set image labels
LABEL project.name="pymake"
LABEL project.version="0.6"
LABEL project.author="Eugenio Marinetto"
LABEL project.author.email="nenetto@gmail.com"
LABEL project.creation="12-05-2018"

# Set the working directory
WORKDIR /usr/src/app

# Clone and install pymake
RUN pip install --no-cache-dir git+https://github.com/nenetto/pymake.git@v0.6 -v

# Define command to execute
ENV TERM xterm
CMD pymake