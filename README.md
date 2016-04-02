# `dev-init` branch

This is the branch for the initial setup of our web app. Final
choice stack?

HTML/CSS/Vanilla Javascript <--> Django <--> Python <--> Firebase

Hosted on heroku

## INITIAL SETUP FOR LOCAL DEVELOPMENT

(I'm assuming you have cloned this repository already)

1. Create this branch locally via `$ git branch dev-init`
2. Switch to this branch via `$ git checkout dev-init`
3. Pull from the remote via `$ git pull origin dev-init`
4. If you have a virtual environment setup up, activate it now.
5. Install dependencies via `$ pip install -r requirements.txt`
6. 

## DEPLOYMENT INSTRUCTIONS TO HEROKU

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