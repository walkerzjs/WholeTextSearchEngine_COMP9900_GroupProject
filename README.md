This program is built on python 3

Installation:

Firstly, add all case data (all html files) to the /static/NSW folder. It will not be included in the submission because of the large file size.

There is a Makefile file under the software folder, it will install packages in requirements.txt and do initialisation then start the server. 


If due to some unseen reason, the MakeFile cannot go through, alternatively, set up and run the system using the steps below:

1. Firstly, run virtual environment and install all supporting external libraries in requirements.txt (i.e. pip3 install -r requirements.txt)

2. Next, run init.py under the software folder(/searchengine/init.py), it will generate related data used for similarity searching (i.e. vectors, vectorizers, processed files).

3. Run searchEngine.py (/searchengine/searchEngine.py), open a web browser, and go to: localhost:9900