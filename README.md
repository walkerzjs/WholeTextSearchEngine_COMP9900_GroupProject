Intro video to Bitbucket: https://youtu.be/0ocf7u76WSo

1. Add your ssh key so that you do not have to enter your password everytime you clone, push, or pull. Bottom left corner, select Bitbucket settings, under SECURITY, select SSH keys and Add key.
2. Clone the repository by doing: git clone git@bitbucket.org:csitproject/searchengine.git
3. Create your own branch (I used my zID as my branch name) to update your work diary. Try to not push into master branch.
4. Try to run searchEngine.py (I ran: "python3 searchEngine.py" in terminal. Need to get some homebrew, python3, and flask in a new OSX laptop).

Important:
1. If master branch is updated, do:
    - git checkout <your_branch>
    - git pull origin master
2. To create a pull request, do:
    - git checkout <your_branch>
    - git branch <new_temporary_branch_name>
    - git checkout <new_temporary_branch_name> (this will create an identical branch to your_branch)
    - include only necessary files that you want to merge to master. remove unnecessary files using rm (e.g. rm file.txt).
    - git add .
    - git commit -m "files to merge"
    - git push origin <new_temporary_branch_name>
    - create a pull request from Bitbucket using new_temporary_branch_name to master branch. (make sure to check the diff to see that the files you want to merge are all included in that new_temporary_branch_name branch)

* Write access to master branch is only scrum master for editing README.md and add some files
* To merge to master branch, 2 approvals is required. Will increase to 3 or 4 if necessary.



additional info:
1. First please copy all the 29907 html documents to the ‘/Legal Case Search App/Legal Case Search App/static/NSW’ folder. There are several existed html documents in the folder but can be ignored. And after this, pycharm may take 20 mins to index the documents.

2. Use pycharm to import the project, need to create a virtual environment or use an existed Virtual Env. There is a file named “requirements.txt” under “/Legal Case Search App” folder. In both situations, please activate the virtual environment, and in the command line, type “pip3 install -r requirements.txt” (the path of requirements.txt may need to be changed) to install required python packages.

3. Because for the sake of reducing uploaded size, all data and vectors are not included, so to use the app, the fresh start is needed. For fresh start, please run the init.py under ‘/Legal Case Search App’, but may require 20-30 mins.

4. After init.py has finished running, can start the server by run the “/Legal Case Search App/searchEngine.py” to start using the app.



Implemented functions for extracting important words for 1-gram and 2-gram features.


Added function of displaying important words produced by tfidf algorithm. and enabled the function of search bar


Stanley and Henri's work:
1. Added functions to login and register.'
