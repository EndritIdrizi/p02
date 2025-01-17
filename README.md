# P02 - Makers Makin' It, Act I - Team JBEE

**Team JBEE** (Jay-Bee)

## Roster:
- Endrit Idrizi **(PM)**
- Ziyad Hamed
- Vedant Kotheri
- Benjamin Rudinski

## Roles: 
Vedant Kothari
- Frontend (CSS + FEF)

Endrit Idrizi
- JavaScript
- Frontend (HTML Templates)
- API Configurations and Connections

Benjamin Rudinski
- Set up Flask and SQLite3 environment

Ziyad Hamed
- Build user authentication functionality
- Middleware file organization
- Build database

## Description:
Our project is essentially a more advanced version of the New York Times ‘Games’ section. It will contain games such as Wordle, Mini Crossword, and Connections. Each of these games will have the same rules and instructions as those found on the official NYT website, but in our website, the kick is that any user can create and customize their own games. In fact, they can publish it to the site to make it accessible for other users to play as well, providing that they are logged in properly. Regarding the APIs, we will be using Merriam Webster Dictionary API. It will be used to check for correctness in words. By logging in, users will have the ability to create their own games as well as view their completed games from the past. We might even implement a feature with credits, where users can earn credits based on the games they play, difficulty, and time played, but this feature will not be possible if you aren’t logged in. In addition, in times of happiness, the following songs could be played as a sign of congratulations: 
- Protagonist - Blanco
- Evicted - Nemmzz
- 4am - JBEE
- SCAR - Song Bird, Gyakie & JBEE
- Talking Stage - JBEE
- Just 4 Me - JBEE
- Changed - JBEE & CRYSTAL MILLZ
- Next Up - S4-E2, Pt. 2 - JBEE
- Heart On Ice - JBEE
- With Me Or Not? - JBEE

Note: NO API KEYS NEEDED
  
---  

## Install Guide [w.i.p]

### Prerequisites
Ensure you have the following installed on your system:
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Python 3](https://www.python.org/downloads/)

It's recommended to run this project in a virtual environment to avoid any potential conflicts with other packages. Obviously this doesn't apply to you Topher, but if your less advanced, refer to [this guide](https://novillo-cs.github.io/apcsa/tools/).

### Steps to Install and Run
1. Clone and move into this repository
```
$ git clone git@github.com:EndritIdrizi/p02.git
```
```
$ cd p01
```
3. Create a virtual environment
```
$ python3 -m venv foo
```

4. Activate the virtual environment: Linux/MacOS
```
$ . foo/bin/activate
```
4. Activate the virtual environment: Windows
```
$ foo\Scripts\activate
```
5. Install required packages
```
$ pip install -r requirements.txt
```
## Launch Codes: [w.i.p]
1. Run the database setup file
``` 
$ python3 app/setup_db.py
```
2. Locate and run the app file
``` 
$ cd app
```
``` 
$ python3 __init__.py
```
3. Access the Application: Open your browser and go to http://127.0.0.1:5000 or click the link that appears in your terminal output.
To stop the app, press CTRL + C
