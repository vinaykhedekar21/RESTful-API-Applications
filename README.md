# RESTful-API-Applications
Back-end Applications with  RESTful API's for the backend applications

Steps to execute the Application-
1. Download/fork project at local.
2. Follow stepsfor database setup and execution

      1. Open the terminals for DiscussionForumAPI and go to directory
		 
         >> cd DiscussionForum-SQLite/DiscussionForumAPI
		 
      2. install the app from the root of the project directory.

         >> pip install --editable .

      3. tell flask about the right application:

       	root@tuffix-vm:/home/student/PycharmProjects/DiscussionForum-SQLite/DiscussionForumAPI# 
	      >> export FLASK_APP=DiscussionForumAPI/DiscussionForum.py

      4. In the DiscussionForumAPI terminal run this:

         >> flask initdb
		 
      5. Also in the same terminal run this to populate the database :

         flask inserScript
	  
      6. Now you can run mini_api:

         flask run



