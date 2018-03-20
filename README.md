# [pymake v2.0](https://github.com/nenetto/pymake.git)

Python package for project creation

## Installation

`pip install setup.py`

## Usage

### 1. Create a `pymakeconfigure.json` ile
```json

{
    "project-name": "Example project",
    "project-description": "Example project description",

    "project-version-major":1,
    "project-version-minor":3,

    "git-repo":"https://github.com/user/example.git",

    "author": "AuthorName AuthorLastName",
    "author-email": "author@mail.com",
  
    "docker-tag": "",
    "type-of-project": "python",

    "configuration":
    {
      "parent-folder": "/where/to/build/your/project",
      "packages": {
        "pack1": {}
      },
      "resource-folders": ["resource1", "resource2"]
    }
}

````

### 2. Run **`pymake`**

`pymake /path/to/your/configure.py

### 3. Learn the structure of your project

- :open_file_folder: **[project-name]**
    - :page_with_curl: `README.md`
    - :page_with_curl: `pymakeconfigure.json`
    - :open_file_folder: **[project-name]**
        - :page_with_curl: `__init__.py`
        - :page_with_curl: `main.py`
        - :page_with_curl: `project_vars.py`
        - :page_with_curl: `pymakefile.json`
        - :open_file_folder: **[resource1]**
        - :open_file_folder: **[resource2]**
        - :open_file_folder: **[pack1]**
            - :page_with_curl: `__init__.py`
        - :open_file_folder: **[pymake]**
            - :open_file_folder: **[docker]**
                - :page_with_curl: `create_docker_image.py`
                - :page_with_curl: `aws_push.template`
                - :page_with_curl: `create_image.template`
                - :page_with_curl: `Dockerfile.template`
                - :page_with_curl: `dockerignore.template`
                - :page_with_curl: `run_container_local.template`
            - :open_file_folder: **[setup]**
                - :page_with_curl: `create_setup.py`
                - :page_with_curl: `setup.py.template`
        

### 4. Develop on your packages

This means that you have to program something!

Some important notes:

#### Resources
>To use resource files on your project, you can access your file path using the library **`pkg_resources`** as:
>
>`pkg_resources.resource_filename(__name__, 'resource.txt')`
>
>Note that this will access files from a python module to a file in the same folder. If the resource is in a deeper folder you can use:
>
>`pkg_resources.resource_filename(__name__, 'path/from/module/resource.txt')`
>
>If you want to access files in upper folders, you have to define the name of your project such as:
>
>**`pkg_resources.resource_filename(example_project, 'resource1/resource.txt')`**
>
>**This option can be used anywhere in your code - MAKE SURE THE ROOT PROJECT FOLDER IS IN `sys.path`**


### 5. Prepare your main function

In the file `main.py`, develop your entry point for your program. Just complete the `main()` function.

### 6. Run `[project-name]/[project-name]/[pymake]/[setup]/create_setup.py`

This file will create the **`setup.py`** of your project in the root directory.

### 7. Run `[project-name]/[project-name]/[pymake]/[docker]/create_docker_image.py`

This script will create the configuration for a docker image creation. **Note** create your **`setup.py`** before the docker image creation.

#### Docker tag

>If you will upload your docker image to an aws repository, make sure your pymakefile.json has the variable **`docker-tag`** set to the repository tag.

#### Create image

>To create your local docker image, run the script **`create_image.sh`** as **root**

#### Test/Run your local image

>Run the script **`run_container_local.sh`** as **root**

#### Push your docker image to the **aws** repository

>Run the script **`aws_push.sh`** as **root**
    
>**The Dockerfile**

>This file is a default that you can modify. It will copy your project folder, install using the `setup.py` and launch your `main` script function

```dockerfile
#"""Project example_project
#Author  Name Surname
#email   me@you.com
#"""

# Set python base image
FROM python:3-stretch

# Set the working directory
WORKDIR /usr/src/app

# Copy files
COPY . example_project/

# Install  internal requirements
RUN pip install --no-cache-dir  example_project/
`
# Define command to execute
CMD [ "example_project" ]
```

## Contact
[E. Marinetto](mailto:nenetto@gmail.com)