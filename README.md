# Git Profile

API that aggregates data from the Github and Bitbucket APIs.

## Getting Started

### Prerequisites

Python 3.6.5

### Installing

`pip install -r requirements.txt`

## Running Locally

`python run.py` will start the devserver, running on `http://localhost:5000`

To avoid getting rate-limited by the Github API, you can add your api token to `config.py`

## Running the Tests

To run the test suite, run `python -m unittest discover tests`
