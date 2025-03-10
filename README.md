# LearnPrivacy

## Overview

LearnPrivacy is a web application that provides an interactive platform to learn about privacy techniques such as K-Anonymization and Differential Privacy.

## Features

- K-Anonymization
- Differential Privacy
- Pseudonymization (Not yet implemented)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- OpenAI dev key

## Installation

### Clone the Repository

```sh
git clone https://github.com/yourusername/privacy-final.git
cd privacy-final
```

### Create and Activate a Virtual Environment

```sh
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### Install dependencies

```sh
pip install -r requirements.txt
```

### Run the app

```sh
python app.py
```

The application will be available at <a>http://localhost:5000</a> or <a>http://0.0.0.0:5000</a>

## Configuration

You will need to create a `.env` file in the directory containing an environment variable for a chatgpt key.

## Directory Structure

```
.env
.gitignore
app.py
dp.py
index.py
kAnonAttempt.py
kAnonymity.py
pseudonymization.py
README.md
requirements.txt
env/
flask_session/
model/
static/
|__ dp.png
|__ k.png
templates/
|__ dp.html
|__ index.html
|__ kAnonymity.html
|__ layout.html
|__ pseudonymization.txt
```
