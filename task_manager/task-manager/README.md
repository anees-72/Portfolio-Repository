# Task Manager
#### Video Demo:  <(https://youtu.be/obxJCgmlogY)>
## Description:

For my cs50x final project I  have created a task management web based application to help people manage their tasks efficiently because in today's busy world there are so many tasks for people to do and it is not uncommon to forget some of those that's why i have created this application to help manage task and do them before due date.
## Files:
Here are the files that are included in my project and their description.
### Static:
In this directory i have included **styles.css** file that contains minimum lines of code as I am using bootstrap mainly for styling and responsiveness in my **syles.css** file I have included some lines of code to change the color of navbar icons and some hover effects and also some margin.Let's now move to templates directory.
### Templates:
In my templates I have several templates for displaying different pages and also different content on those pages.Here are the templates that i have included in my project.
#### Layout.html
The main template for all the other templates and to which all the other files extend in this main template I have used the bootstrap navigation bar classes to make an interactive navbar to go to differnt pages of my website and access different features by visiting there I have also used **get_flashed_messages()** function to display the flash messages passed from app.py in the head section of my templates.
#### Login.html
The page that is first shown when the user visits my site and I have used bootstrap **card** class to display the **login form** to the user where the user can add their username and password to enter the application and if the user don't have an account already then there is a link on the bottom to go to registration page and also in the navigation bar the user see login and register button to go there.
#### Register.html
This is the page that is shown to the user when the user clicks on register here button I have also used the bootstrap **card** class to display the registration form and after making an account the user is redirected to the login page to login and then go to the main application.
#### Index.html
This is the main page that the user see when they log in on this page I have created a dashboard table where the user see their current tasks their status and priority and i have used different classes to make the table interactive and I have also included several other options for the users like **filter by priority** and **search the task by title** and **sort by date ascending or descending** and and **apply filter** button to apply the filters.In the table I have included several options for the users in the action column of the table where the users can **mark the task as completed** and **edit the task** and they can also **delete the task** from the table.I have also used cards to display the **completed tasks,pending tasks and overdue tasks** and have given different colors to those card for symbolizing different kinds.
#### Create_task.html
In the navigation bar after the dashboard option there is a option by the name of **Create Task** via which users can create new tasks when the user clicks on this option a new page open and that displays a form on the card to enter the details of the task to be created such as **title,description,priority and due_date** and a create task button to create the task and when the user clicks on that button after entering all the details the task is created and it goes to the dashboard table where the user can see it.
#### Edit_task.html
This files looks same as create task template when the user clicks on the edit task option on given in actions column of the dashboard tasks table then the edit_task.html template is loaded with all the details of the tasks which is clicked to be edited with the same options as in the create task template.
#### History.html
This is the template that contains table that displays all the tasks that have been marked completed in the dashboard table when the user clicks on the mark as completed option in the dashboard table the tasks disappears from the dashboard table and goes to history table in the history.html user can see it by clicking on the history option in the navigation bar.
#### Calender.html
I have also included the see in **calender option** in my web based application to help the users see their tasks in the calender form i have used full calendar library and additional javascript to display the task in the calender which provides good user experience.The users can click on the see in calender option in the navigation bar to see their pending tasks in the calender interface.
#### Apology.html
And finally I have apology.html template for displaying the  error messages with the error code that are passed from app.py and i have used bootstrap card classes to display error messages in a more interactive way.That's for my project's template directory and now I will explain the working of main application **app.py** supported by **helper.py**.
### App.py
This is where the main backend code goes in this file i have imported several modules and function from flask to perform several functions this is the application where all the **templates are rendered**,**login** and **logout** functionalities are performed by using flask session and by clearing it,**redirects** takes place based on several condidtions all the routes are handled here by **querying the database** and passing the data back to templates for showing in tables or updating the existing one's this app perform main function such as linking the database and managing the session and storing the user's password using **generate_password_hash** functions to store the hash of user password in the users table and indeed all the data displayed in tables on the front end comes from here based on condition and **filter applied and search query** all those functionalities are handled from here.I have used dynamic sequel queries to query the database based on the condition and fetching the data from there if those conditions hold.Indeed all the backend logic goes here.
### Helper.py
This is the file that helps the app.py in working two functions that are defined here which are **login_required** and **apology** are used in the app.py for performing operation such as giving access to user to the main application only when he/she is logged in and returning apology based on several errors and conditions.
### App.db
And finally I have app.db(database for this application) to store the information of users and tasks.That's it for my final project.

