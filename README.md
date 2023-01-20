# talis-library
A collection of scripts for use with Talis Aspire API version 3.

These are scripts that I have written and used in my role as Discovery and Systems Manager at Solent University Library. I am a librarian who does some scripting for his job; I AM NOT A PROFESSIONAL SOFTWARE DEVELOPER, so the scripts are certainly unsophisticated and probably flawed in some way. However, they have all been used many times at Solent University, so it struck me that they may be of use to others. Indeed, the fact that they were written by an amateur may make them of more use to other amateur scripters than professional code - they may be more comprehensible.

That said, you use these scripts at your own risk. You'll need to know Python basics before using them (and have Python installed), and you should read through the code to make sure it does what you want. You should also check out the Talis PAI docs at https://rl.talis.com/3/docs, and speak to the Talis develper team before using the API (you'll need to get the authentication details from them anyway). There is a weekly developer meeting that the team at Talis organise, so you could take any project you want to do to them; there will probably be a better way of doing it than using my scripts.

There is a main file, talis.py, that serves as a module file. In here I include small functions that I use repeatedly. When I want to do a specific project, I call this file with the following lines of code in my project script:

import sys

sys.path.append('C:\\Users\\clarkj\\OneDrive - Solent University\\PythonModules')

import talis

My work laptop is locked down, so I can't add the directory where I store this file to the path permanently; I have to do it for every script using the first two lines above. Then I just import the talis module, and call the functions as with a normal module, e.g., talis.createDraftItem(body).

The functions and how they work are, I think, all self explanatory. So instead of creating separate documentation, I suggest you take a look at the code itself to identify potentially useful functions. There are comments in there to elucidate certain bits. In particular, there are three places where you need to add your own information:

1. api_base = "YOUR API BASE URL HERE" ## e.g., https://rl.talis.com/3/solent/
2. secret_key = 'YOUR CLIENT ID HERE' + ':' + secret
3. headers['X-Effective-User'] = 'YOUR USER ID HERE'

I think it is clear why (1) is needed. Authentication is done via client ID and client secret. I have chosen to hard code my client ID in the script (2), but for extra security the secret is prompted each time the script is run, and I keep this safe elesewhere. The user ID is needed for some opeations (publishing lists, I think), but I find it easier to hardcode it into the script everytime, as in (3). Any time this script does something that need the user recording, it records it as me doing it, which is fine for the way I use the script. You can get your ID from the All User Profile report on your tenancy, under the Talis Global User ID column.

The directories in this repository are examples of projects that use this module file.
