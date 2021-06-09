# Introduction

The project contains a task to pull data off [xkcd](https://xkcd.com/) and stores into 
MySQL database.

# Setup
-   Create virtualenv

```
virtualenv venv
# `virtualenv -p=python3 venv` (If `Py3` is not the default version)
```
-   Activate virtualenv 
```
source venv/bin/activate
```

-   Install dependencies (using virtual environment is recommended):
```
pip install -r requirements.txt
```

-   `mysql` database installation - 

https://tecadmin.net/install-mysql-8-centos-8/

Note : This project has been tested against `mysql-8.0.21` using `RHEL8.4`.
We recommend `yum` installation for RPM-based software installations.
More instructions for [installing MySQL on Linux](https://dev.mysql.com/doc/refman/8.0/en/linux-installation.html). 

**Database setup instructions -**

-   To setup, database use sql script `database_.sql` (contains DDL).
-   You should create a file as `commons/settings/secrets.yaml` to contain database credentials

```
# ---LOCAL---
LOCALSQL_USER: root
LOCALSQL_HOST: 127.0.0.1
LOCALSQL_PORT: 3306
LOCALSQL_PASSWORD: xxxxx
LOCALSQL_DATABASE: xkcdDB
```

NOTE: `pymysql` [installation](https://pymysql.readthedocs.io/en/latest/user/installation.html) and 
related versions of `mysql` should be matched.

# Usage
-   Activate virtual env `source venv/bin/activate`
-   Start the app with `python task_one.py`

Good luck!

# Running tests

[TODO] to be added soon.

# Development notes


    The database modeling for the xkcd API goes like follows: 
    Name of models -
    
    # comics    
     
    num: INT(11) NOT NULL PRIMARY KEY
    month: VARCHAR(250)
    link: VARCHAR(250)
    year: VARCHAR(250)
    news: VARCHAR(250)
    safe_title: VARCHAR(250)
    transcript: VARCHAR(5000)
    alt: VARCHAR(5000)
    img: VARCHAR(250)
    title: VARCHAR(250)
    day: VARCHAR(250)
    
    NOTE : Readers are requested to raise PRs with `problems identified` with the script.

# coding style

-   Since the code has been written in Python3.x, function annotations and type-hinting has been  
    used across.
-   Google-Styled docstrings have been used to describe functions/classes/modules.
-   Pydantic data-classes have been used to validate the responses from xkcd API endpoints.
-   Set your IDE character limit per line to maximum 100 (recommendation)
-   Set your configurations via ``common/settings/secrets.yaml``; Do *NOT* commit file containing secrets.
-   The generic functionality has been maintained under ``commons``.
-   An independent data access layer (`commons/dal.py`) has been created to isolate data retrieval and storage
 functionality.
    
# Task 1

1. GET 15 random comics and following details in using Python.
    - Get the names of the comic
    - Get the alt-text of the comic
    - Get the number of the comic
    - Get the link of the comic
    - Get the image of the comics
    - Get the image Link of the comics

2. Insert into MySQL - Please include SQL database schema(s) for any table(s) created in
your Github repo
    
**OUTPUT OF TASK 1  (as of timestamp: '2021-06-09 18:31:20')**
```json
[
  {
    'comic': "Stacey's Dad",
    'comic_meta': {
      'alt_text': "I bet she gets you to mow the lawn, doesn't she?",
      'number': 61,
      'link': 'https://www.xkcd.com/61',
      'image': 'staceys_dad.jpg',
      'image_link': 'https://imgs.xkcd.com/comics/staceys_dad.jpg'
    }
  },
...,
...,
  {
    'comic': 'Valentine - Karnaugh',
    'comic_meta': {
      'alt_text': 'Love and circuit analysis, hand in hand at last.',
      'number': 62,
      'link': 'https://www.xkcd.com/62',
      'image': 'karnaugh.jpg',
      'image_link': 'https://imgs.xkcd.com/comics/karnaugh.jpg'
    }
  }
]
```

# Notes/Warnings

Random number generator may produce some integers IDs within `range(1, 87)` which may not yield any
results from xkcd API (404s). In which case, we skip those IDs and store the rest.


# Future scopes

    ** [TODO] try another approach ** - 
    
    Crawl through all the urls from xkcd API first, resolve dependecies endpoint-by-endpoint 
    and store into record tables.
    Finally, use local database to produce results per ask in the task.
                       