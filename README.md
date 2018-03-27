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
