# group-polls
Users can create or join existing groups and create polls and vote in active polls in that group

## Features
The minimum amount of functions
#### Login page
The user can log in with existing credentials or create new credentials

#### Group listing / main page
* A listing of existing groups is shown.
* The user can create new groups.
* Opening a group redirects to the group view.
* The user can easily distinguish which groups they have already joined.
* In the poll listing, a timer is shown if the poll is active, and if the poll has ended it is signified in another way.

#### Group
* A list of existing polls for the group is shown. 
* The user can create new polls.
    * The user can give a name and a description and determine an end time for the poll.
* Opening a poll redirects to the poll view.
* Group name, number of members

#### Poll
* A listing of existing choices is shown.
* The user can add a vote (or retract their vote) for each choice.
* The user can create new choices for the poll.

### Future development
Ideas for future development

#### Group
* Ability to lock group and accept and kick members for the group founder.
* Group creator can delete the group.

#### Poll
When creating a poll, the user can configure various properties for the poll.
* Multichoice polls and single-choice polls.
* Hide/show results if the user has not voted.
* Lock the poll so that users can't add choices.
* Poll creator can delete the poll and modify poll properties.

## Setting up
1. Clone the project to your computer:
```
git clone git@github.com:mko3000/group-polls.git
```
2. Go to the root folder of the project and start the virtual environment with
```
python3 -m venv venv
source venv/bin/activate
```
3. Install the dependencies with
```
pip install -r requirements.txt
```
4. Initialize the database with
```
psql < schema.sql
```
5. You can add some mock data to the database with
```
psql < mockdata.sql
```
The mock data includes some user profiles, for example "batman" and "ironman". All the mock profile passwords are "key123".

6. Launch the app with
```
flask run
```

## Notes about the implementation
The methods ```polls.poll_stats``` and ```polls.poll_winner``` have been implemented with a complex sql query even though a python implementation would have been simpler. The motivation for this choice is to showcase my ability to formulate complex sql queries as this project is part of a course about databases and web programming.