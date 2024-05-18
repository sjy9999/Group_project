# Agile Assignment 2

This is our Agile Assignment 2.

## Group Member

**Name:**  QuanDi Liu
**ID:** 24129104  
**GitHub Username:** andyhimself22

**Name:** Junyi Sun  
**ID:** 24382608  
**GitHub Username:** sjy9999

**Name:** Brandon Ge  
**ID:** 23813666  
**GitHub Username:** bag026

**Name:**  Yuanfu Cao
**ID:** 23633858  
**GitHub Username:** Cyf1160819266


## Prerequisites

This application is designed to run using Python (version 3) within a virtual environment. It leverages the Flask framework for web development and SQLite for the database. To set up the virtual environment and install the required packages, please follow the instructions in the `requirements.txt` file.

## Installing

1. **Create a Virtual Environment:**
   - Use `pip` or another package manager to install the `virtualenv` tool:
     ```sh
     pip install virtualenv
     ```
   - Activate the virtual environment:
     ```sh
     source venv/bin/activate
     ```
   This setup will include Flask and all necessary packages.

2. **Install SQLite:**
   - **Windows:**  
     Download and install SQLite from the official website.
   - **Linux:**
     ```sh
     sudo apt-get install sqlite3
     ```

3. **Set Up the Database:**
   - Initialize the database and start the application:
     ```sh
     flask db init
     flask run
     ```


<!-- 1 Would you like to know how to start it?  -->
It's quite simple. Have you seen app.py? Click on it, then click "Run".

Inside, there are different modules.

### 1
First, for registration and login, each username corresponds to one email, and no one else can use the same username and email. This prevents duplicate usernames. If you forget your password, you can click the "Forgot Password" button and enter your email. You will receive a link in your email, which you can follow to update your password.

Note that the email must match the one you used during registration. For example, if your username was 9 and your email was 9@qq.com, you must enter the same email, it is 9@qq.com. This is to prevent someone else, like AAA using their own email AAA@qq.com, from resetting the password for 9. Thus, if 9 forgets their password, they should enter 9@qq.com.

Additionally, on the left side, there are some scrollable images showcasing beautiful pictures, serving purely as decoration. There are also features such as showing or hiding passwords.

### 2
Upon entering the main page, our project is called Swan-forum. This is a forum where people can freely express their opinions. On the right side of this image, a brief introduction to the app's functions is given, such as "Function 1 of APP," "Function 2 of APP," etc. The left side of the main interface has several buttons that lead to new pages.


### 3
Now entering the "Create Post" interface, here you can start a request. For example, title it "goat," and then in the Description, enter the content you wish to describe, such as "Who do you think is the king of football?" By clicking submit, you can post your request. If you decide not to post at that moment, clicking "back to main page" will take you back to the main interface.


### 4
Now entering the "Search requests" interface, here you can search for posts. Initially, this project will display some posts made by others, allowing you to browse what they have discussed. You can see their replies and who replied. For example, a post titled "who is the goat," Peter replied "Messi," Jack replied "Ronaldo," and Rose replied "Jordan." 
If you have a specific target, like searching for "goat," all posts related to "goat" will be shown, and you can also share your opinion, like your answer might be "Tim Duncan" or "Kobe." By clicking submit, you can post your reply, and others can see your response.
Of course, if you search for Brunnswick, a small town in the UK, you'll find it's not popular yet. No posts about it and no replies below.


### 5
Then in the ranking interface,user ranking system with a corresponding ranking chart, ranking users based on their scores and visualizing the data in a chart format. The main features include a user ranking table showing rank, user ID, name, and score, alongside a ranking chart for visual representation of user scores. The interface also includes a "Back to Main" button for easy navigation.


### 6
In the The profile settings page includes user details such as name, bio, email, and last seen time, with an option to update the profile picture via Gravatar. The user ranking section prominently shows the user's rank, score, and a congratulatory message for top 3 positions. Additionally, users can edit their bio for personalized profile information, and customize their theme color for a personalized experience. The current weather section provides real-time weather updates including location, temperature, description, humidity, and wind speed. The user requests section allows users to view and manage their requests. For enhanced user support, a live chat option is available. Navigation is made easy with "Go Back" and "Logout" buttons.

### 7
The Swan-Forum Guidelines section promotes community standards, encouraging respectful interactions, avoiding spam, and sharing valuable content.


## Refelection
### Some changes about this program have resulted in a lot of unnecessary work.
At the beginning, this project used SQLite3, but later changed to SQLAlchemy. CSRFProtect was not initially included, but later added, which led to many changes in both frontend and backend. Flask-Login functionality was not used initially, and a custom login function was implemented instead. Later, this was also changed to meet the course requirements for Flask-Login. These changes consumed a lot of redundant time.

### Achievements
We successfully completed the project, ensuring that it runs without errors or bugs. This achievement is significant, given the constraints we faced.

### Challenges and Constraints
We also have other courses besides CITS5505, specifically three courses with assignments assigned on May 6th and due on May 20th. Within this 14-day period, we had to start from scratch and complete three entirely new assignments. Additionally, these assignments are the final ones of the semester, making them the most challenging and comprehensive. This tight schedule left us with very limited time.

### Future Improvements
While the project is functional, we recognize that there are areas for improvement. Given more time, we would focus on enhancing the code quality to achieve higher cohesion and lower coupling. Additionally, we have identified features that could further enhance the project and more interactive with user,
like allowing users to follow each other to foster a more interactive community or enabling users to send messages to each other to improve communication and engagement.These improvements would contribute significantly to the overall architecture and maintainability of the project.

### Final Thoughts
Despite the time constraints and challenges, we are proud of what we have accomplished. We have learned a great deal through this process and look forward to applying these lessons in future projects.

## Contributing
For guidelines on our code of conduct and instructions on how to submit pull requests, please refer to 'contribution'.


Hope you like it!