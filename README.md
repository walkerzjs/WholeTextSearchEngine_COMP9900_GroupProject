This program is built on python 3

Installization:

Firstly, add all case data(all html files) to the /static/NSW folder. It will not be included in the submission because of the large file size.
There is a Makefile file under the software folder, it will install packages in requirements.txt and do initialisation then start the server. 


If due to some unseen reason, the MakeFile cannot go through, alternatively, can setting up and running the system through next steps:
1. Firstly, run virtual environment and install all supporting external libraries in requirements.txt (i.e. pip3 install -r requirements.txt)
2. Next, run init.py under the software folder(/searchengine/init.py), it will genenrate related data used for similarity searching (i.e. vectors, vectorizers, processed files).
3. Run searchEngine.py(/searchengin/searchEngine.py) and open browser, go to: localhost:1345
