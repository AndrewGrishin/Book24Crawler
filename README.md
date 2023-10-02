# Crawler Project

## Introduction

Books24 is a paperback book shop that allows uses to make purchases online, select shipping address and leave reviews. This project provides a simple CLI (Command Line Interface) API for [Books24](https://book24.ru) service that allows user to send requests from the terminal. After request is done the programme forms JSON file with all information about each book found according to the initial query.

## About the project

In this project [Books24](https://book24.ru) is going to be analyzed. The main target of this project is to provide convinient API for this site by using which any user will be able to get information of all books he/she requested.

The project development is devided into 3 global parts.

- [x] Making request to the site (user side).
- [x] Book information gatherment (crawler side).
- [x] Converting into JSON format (output).  

## Data we are looking for

Data that is going to be collected from the server about each book contains:

- [x] Links on the page.
- [x] Title of the book.
- [x] Author.
- [x] Classification.
- [x] Description.
- [x] Price.
- [x] In stock amount (verbal).
- [x] Vendor code.
- [x] Stars.
- [x] \# of starts reviews.
- [x] \# of textual reviews.

## User guide (Unix systems: Linux, MacOS, ...)

- Create directory.
- Place files ```Scraping.py``` and ```RequiredFunctions.py``` into that folder.
- Open terminal and create ```virtualenv```.
- Activate it via: ```source <virtualenv_name>/bin/activate```.
- Install required packages:  ```pip install fake_useragent requests beautifulsoup4 tqdm```.
- Open terminal and enter the following command ```python Scraping.py <your request>```.
- As a result you will get ```.json``` files with the structure.
