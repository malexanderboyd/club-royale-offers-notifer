# Royal Casino Tracker

This is a simple Python project that uses web scraping to check for new offers from Royal Caribbean's Club Royale website.

It will send a desktop notification using winotify if a new offer is found.

## Requirements

- Python 3.10 or later
- Redis server (can be installed locally or via Docker)
- Windows 10 or later (for desktop notifications)

## Installation

1. Clone this repository.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Make sure Redis is running. If you're using Docker, the redis container will start during the `run.ps1` script.


## Usage

You can pass in a list of last names and reward numbers to check by running `.\run.ps1 -check "lastname1,rewardnumber1 lastname2,rewardnumber2"`. Separate each name and number pair by a space.

The scraper will write a log file named `last-ran.txt` in the current directory with an ISO 8601 formatted timestamp for when it was last run.


## Author Notes

The majority of this was built by chatgpt-3, including this readme.