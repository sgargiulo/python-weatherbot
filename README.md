# Python Weatherbot

A weaterbot used to obtain forecasts and suggested equipment for the day such as an umbrella and/or sunblock. 

## Prerequisites

  + Anaconda 3.7
  + Python 3.7
  + Pip

## Installation

Fork this repository under your own control, then clone or download the resulting repository onto your computer. Then navigate there from the command line:

```sh
cd weatherbot
```

> NOTE: subsequent usage and testing commands assume you are running them from the repository's root directory.

## Environment Setup

Use Anaconda to create and activate a new virtual environment, perhaps called "weatherbot-env":

```sh
conda create -n weatherbot-env python=3.7 # (first time only)
conda activate weatherbot-env
```

Then install the requirements
```py
pip install -r ./requirements.txt
```

## Setup Continued

You'll need API keys for the Geocodio API and Dark Sky API. An .env-sample file has been provided for you -- you can just duplicate it and name it `.env`

You can sign up for a Dark Sky API key at https://darksky.net/dev/register. You can sign up for a geocodio API key at https://dash.geocod.io/register


## Usage

Start the bot

```sh
python bot.py
```
Enter in zip code or city, state

If an invalid entry is entered, you will be notified and have to try again.

## [License](LICENSE)
