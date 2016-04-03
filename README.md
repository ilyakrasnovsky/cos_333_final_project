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
