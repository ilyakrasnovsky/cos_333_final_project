
# COS 333 Final Project

HIS CAREFULLY**. If you disagree with any of this, please bring it up on our Slack page, and we'll discuss/amend. Also, if you are not familiar with Github, **PLEASE CONSULT** with a team member who is so as not to mistakenly break something.

### I. `master` branch

Consider `master` to be the branch that we submit at the end of the semester. As such, **NOTHING** gets pushed there unless it has been **THOROUGHLY TESTED** and deemed stable by the project manager (PM). In fact, I propose that **ONLY THE PM** has the right to push to `master`.

### II. `dev` branch

`dev` is the branch where we **ASSEMBLE** our latest version at any given point. As such, **DO NOT DEVELOP** on this branch. You should be developing/testing your piece(s) in a separate branch **OFF OF** `dev`. When you feel like you have successfully implemented and tested all of the functionality in your branch, you are ready to merge your branch with `dev.` (see IV.)

### III. Individual Branches Off of `dev`

Note that these have not been created yet, but will be soon once we've established who is writing what. The rules here are pretty freeform, commit and push your regular work to your individual branch(es), and try to maintain consistent documentation (see V. and VI.) This is where the majority of your time is expected to be spent.

### IV. Merging into `dev`

Once you have finished writing and testing your feature in your individual branch, and you are confident that it is ready to be used by others, you can merge it into `dev`. When you do this, you should have a **THOROUGH, DESCRIPTIVE** message that details what it is that you're adding, a well-commented API of your piece, example usage, and any potential issues that you foresee.

Further, I propose that when you do this, you also **NOTIFY THE ENTIRE TEAM** (by email or Slack) that you merged with `dev`. Everyone can then update their individual branches by pulling from `dev`. Ideally, work continues uninterrupted for everyone, and you can pick up the next part of the project in a new individual branch. Realistically, something breaks for someone after they pulled, and it is then your responsibility to collaborate with said someone to resolve the issue. 

### V. Commit messages

This follows III. in being pretty freeform, but try your best to commit to your individual branch **OFTEN** (good version control), and having a **CONCISE** commit message of what you just did. A good example is "Implemented the getTokens() method in the Parser() API." These should be happening much more often than merges, so accumulate the finer details into your merge message (see IV).

### VI. General Comments, Interfaces, and APIs

Also pretty freeform, but I propose that we have at least a loose structure of commenting. For instance, every class and method should have a comment with a name, description, instance variables, inputs/outputs (and their data types), somewhere near it. For example (in Python):

```python

'''
class : Token

description : a Token data type stores information in the form
				of a string and can get you its length 

instance variables :
	content : the Token's content (string)
	length  : length of the Token (int)

constructor variables
	input   : the content that the Token will store (string)

available functions : 
	getLength()
'''

class Token:
	def __init__(self, input):
		self.content = input
		self.length = len(input)

	'''
	function : getLength

	description : returns the length of this token

	inputs:
		none

	outputs:
		length : length of this token (int)
	'''
	
	def getLength(self):
		return self.length
```

When merging with `dev`, come up with an "extra good" version of this for the API you are giving to other teammates. We want to make it as easy as possible to utilize each other's code. Example usage in a fake `main()` method goes a long way.

With all this said, let's have a great time and build something **AWESOME**.
=======
# `dev` branch

Development branch, latest stable releases here

This is the branch for the initial setup of our web app. Final
choice stack?

HTML/CSS/Vanilla Javascript <--> Django <--> Python <--> Firebase

Hosted on heroku

## INITIAL SETUP FOR LOCAL DEVELOPMENT

(I'm assuming you have cloned this repository already)

1. Create this branch locally via 
	
	`$ git branch dev-SOME_NAME_HERE`

2. Switch to this branch via 

	`$ git checkout dev-SOME_NAME_HERE`

3. Pull from the remote via 

	`$ git pull origin dev`

4. If you have a virtual environment setup, activate it now.

5. Install dependencies via 

	`$ pip install -r requirements.txt`

6. Go to the project directory via 

	`$ cd project`

7. Go to our Heroku app dashboard for assign-cals-cos333, click
on "Settings", then "Reveal Config Vars". You will see our codes
for SECRET_KEY and FIREBASE_KEY.

8. In command line, run: 

`$ python localcreds.py 'SECRET_KEY_CODE_HERE' 'FIREBASE_KEY_CODE_HERE'`

(Note the quotes around both, and the order of the two)

9. You can now develop!

10. To test locally, you have two options:

	`$ python manage.py runserver` (the Django way, app will be on localhost:8000)

	OR

	`$ heroku local` (the Heroku way, app will be on localhost:5000)

11. While you're developing but not yet ready to push to `dev`, save your work in your branch via:

	`$ git add -A`

	`$ git commit -m "COMMIT_MESSAGE_HERE"`

	`$ git push origin dev-SOME_NAME_HERE`

(Note that SOME_NAME_HERE has to match the one you made in step 1)

## DEPLOYMENT INSTRUCTIONS TO HEROKU

1. Test your changes locally to make sure everything works
(we will use Django tests.py unit tests soon, but not right now)

2. In the `project/settings.py` file, make sure that `(SECRET_KEY, FIREBASE_KEY) = SECRET_KEYS('REMOTE')` and that `DEBUG = False` 

3. Push your changes to `dev` via:

	`$ git add -A`

	`$ git commit -m "COMMIT_MESSAGE_HERE"`

	`$ git push origin dev`

4. Go to our Heroku app dashboard, click on "Deploy", scroll down to "Manual Deploy", make sure `dev` is selected, and click "Deploy Branch".

5. If the build succeeded, you will see an update in the "Activity" Tab on our dashboard, and your changes should be updated at assign-cals-cos333.herokuapp.com/
