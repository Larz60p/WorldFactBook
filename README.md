# WorldFactBook
WorldFactBook

The CIA World Factbook contains a plethora of information on Countries of the world, and is in public domain so you can use this information in your applications.

This package scrapes the Factbook and stores the results in a single JSON file.

Initial directory setup
First if you don't have pyenv installed, please do so, follow tutorial here: https://python-forum.io/Thread-Part-1-Linux-Python-3-environment?highlight=pyenv

* Create a directory named CIA-FactBook (case sensitive) where you want your source code
* Cd to CIA-FactBook
* Run: python -m venv CIA_venv
* Activate virtual environment, run: . ./CIA_venv/bin/activate
*
* Need to install some packages:
*   pip install --upgrade pip
*   pip install pylint
*   pip install cssselect
*   pip install lxml
*   pip install BeautifulSoup4
*   pip install selenium
*   pip install requests
*
* Run: python ScraperPaths.py one time to create directory structure
*
* Run main program: CIA_FactbookMaster.py

