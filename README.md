# Classic Confectionery

An e-commerce sweet shop.
___
## Table of Contents <a name='contents'></a>

* [User Experience (UX)](#userexperience)
* [Design](#design)
* [Web Marketing](#marketing)
* [SEO](#seo)
* [Development](#development)
* [Database Schema](#database)
* [Existing Features](#existingfeatures)
* [Features Left to Implement](#toimplement)
* [Testing](#testing)
* [Unfixed Bugs](#bugs)
* [Deployment](#deployment)
* [Create a Clone](#clone)
* [Technologies Used](#tech)
* [Credits](#credits)
___
### User Experience (UX) <a name='userexperience'></a>

**Site Goal**


**Target Audience**


**Owner Goals**


**How These Goals are Addressed**   


**Data Required**


**Security Features**


[Return to Table of Contents](#contents)
___
### Design <a name='design'></a>

- **Color Scheme**


- **Typography**


- **Imagery**


- **Layout**


[Return to Table of Contents](#contents)
___

### Web Marketing <a name='marketing'></a>

* Strategy

* Newsletter

* Facebook Business 

[Return to Table of Contents](#contents)
___

### SEO <a name='seo'></a>

* Keywords

[Return to Table of Contents](#contents)
___
### Development <a name='development'></a>

*The project was developed using an agile methodology, with epics broken down into user stories with well defined acceptance criteria, tasks and wireframes. These issues where then worked on in incremental steps. The sprint times for my iterations was two weeks. The story points applied to my issues follow the fibonacci scale, with the 'Must Have' issues for each iteration kept at 60% of the total time box.*

- **Product Backlog**
    * The product backlog for the project can be found [here](https://github.com/LewisCM14/sweet-shop/milestone/1)

- **Iteration 1**
    * The iteration 1 milestone can be found [here](https://github.com/LewisCM14/sweet-shop/milestone/2)
    * Iteration 1 board can be found [here](https://github.com/LewisCM14/sweet-shop/projects/1)

- **Iteration 2**
    * The iteration 2 milestone can be found [here](https://github.com/LewisCM14/sweet-shop/milestone/3)
    * Iternation 2 board can be found [here](https://github.com/LewisCM14/sweet-shop/projects/2)

- **Iteration 3**
    * The iteration 3 milestone can be found [here](https://github.com/LewisCM14/sweet-shop/milestone/4)
    * Iteration 3 board can be found here [here](https://github.com/LewisCM14/sweet-shop/projects/3)

- **Iternation 4**
    * The Iternation 4 milestone can be found [here](https://github.com/LewisCM14/sweet-shop/milestone/5)
    * Iteration 4 board can be found here [here](https://github.com/LewisCM14/sweet-shop/projects/4)

[Return to Table of Contents](#contents)
___

### Database Schema <a name='database'></a>

[Return to Table of Contents](#contents)
___
### Existing Features <a name='existingfeatures'></a>

[Return to Table of Contents](#contents)
___
### Future Features <a name ='toimplement'></a>

*The product backlog can be viewed [here](https://github.com/LewisCM14/sweet-shop/milestone/1).*

[Return to Table of Contents](#contents)
___
### Testing <a name ='testing'></a> 

- **Bugs found in Development**

    ---

- **Validator Testing**

    - HTML
        - No errors were found when passing through the [W3C Validator tool](https://validator.w3.org/nu/)

    - CSS
        - No errors were found when passing through the [W3C Validator tool](https://jigsaw.w3.org/css-validator/)

    - JAVASCRIPT
        - No custom Javascript is used in the project, so validator testing was not required.

    - Python
        - No errors were found when passing through the [PEP8 Validator tool](http://pep8online.com/).
    ---

- **Lighthouse**

    ---

- **Automated Tests**

    * Using the coverage package, i have generated reports for the app

    ---

- **Running the Automated Tests**

    * Within the terminal on the IDE run the below command, this runs the automated tests.
        
            coverage run --source=**app name** manage.py test
    
    * Once the tests are complete, run the below command to generate the report.
        
            coverage report
    
    * To then view the report in detail run the below command, which will either create or update the *htmlcov* directory.
        
            coverage html
    
    * To view this report in detail use the below command to launch a basic html server and navigate to the *htmlcov* directory in the browser.
        
            python3 -m http.server
    
    * If you do not wish to view the coverage report but simply want to verify all the test's pass, preform the below command and the results will be printed back to you in the terminal.

            python3 manage.py test
    
    ---

- **Manual Testing**

    * Using devtools on google chrome the application has been tested on various devices to ensure it is fully responsive. 
    
    * Outside of devtools i have ran the site on several browsers including: Brave, Chrome, Firefox and Edge. It appears to function as intended on these browsers. I have also ran it on my own personal pc, laptop and iphone, preforming as intended on each.

[Return to Table of Contents](#contents)
___
### Unfixed Bugs <a name ='bugs'></a>

[Return to Table of Contents](#contents)
___
### Deployment <a name ='deployment'></a>

- The site is deployed via [Heroku](https://heroku.com/). The steps to deploy are as follows:

    *It is assumed the GitHub repository for the project is setup correctly as this point.*
     
    *Ensure all requirements for the project are added to the requirements.txt file prior to deployment. The command **pip3 freeze --local > requirements.txt** can be ran in the terminal to do this.*

    *It is also assumed that the Django project is setup as intended, necessary dependencies installed with all apps required added to the INSTALLED_APPS variable within settings.py. For this project the booking app is all that is required.*

    * STAGE ONE - Create a New App in Heroku

        1: From the dashboard on Heroku, select New and then Create new app.
        
        2: Enter an individual app name into the text box, select a relevant region from the dropdown and then press Create app.
        
        3: A Heroku app has now been created.
    
    ---
    
    * STAGE TWO - Add a Database

        1: Navigate to the resources tab for the app that has just been created.

        2: In the Add-Ons section, search for the Heroku Postgres add on and submit an order form.
        
        3: Select the Settings tab for the app.

        4: Reveal Config Vars and copy the DATABASE_URL string provided.

        5: Create a env.py file within the project and use the copied string to create a DATABASE_URL environment variable. The Python OS module will be required for this.

        *The env.py file is used to protect keys which should only be viewed by the developer. This file will not be pushed to GutHub for public display.*

    ---
    
    * STAGE THREE - Create a SECRET_KEY

        1: Within the env.py file, create a SECRET_KEY environment variable. The string for this variable is decided by the developer.

        2: On the settings tab of the Heroku app, reveal config vars and add the SECRET_KEY variable along with the corresponding string.

    ---
    
    * STAGE FOUR - Update the settings.py file

        1: Import dj_database_url and env.py into the settings.py file within the project.

            import dj_database_url
            if os.path.isfile('env.py'):
                import env

        2: Update the default SECRET_KEY variable provided by Django to the SECRET_KEY environment variable.

            SECRET_KEY = os.environ.get('SECRET_KEY')

        3: Using an if/else statement update the DATABASES dictionary for the deployed project to use the DATABASE_URL environment variable, the dj_database_url library is utilized here.

            if development:
                DATABASES = {
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': BASE_DIR / 'db.sqlite3',
                    }
                }
            else:
                DATABASES = {
                    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
            }
        
        *The database for developing the project remains as the sqlite one provided*

        4: Preform a migration.

        *The Heroku database is now being used as the backend, within the resources tab of the app, the Heroku Postgres link will bring up a window demonstrating this.*

    ---

    * STAGE FIVE - Connect app to AWS

    ---
     
    * STAGE SIX - Tell Django where the templates are stored

        1: Under the BASE_DIR on settings.py, add in the below templates directory. 
        
            TEMPLATES_DIR =  os.path.join(BASE_DIR, 'templates')
        
        2: Then within the TEMPLATES setting, update the DIRS key to point towards this variable.

            'DIRS': [TEMPLATES_DIR]
    
    ---
    
    * STAGE SEVEN - Update ALLOWED_HOSTS

        1: At this point, within settings.py, set the DEBUG variable to development.

        2: Using an if/else statement update the ALLOWED_HOSTS variable for the deployed project to be the name of your Heroku app with ".herokuapp.com" appended to the end.

            DEBUG = development

            if development:
                ALLOWED_HOSTS = [
                    'localhost',
                ]
            else:
                ALLOWED_HOSTS = ['sweet-shop-lewiscm.herokuapp.com']

        *For development the host is set to localhost, so that the project can be ran locally. This is also a good point to add the Media, Static and Template directories, these folders should be added at the top level.*
    
    ---
    
    * STAGE EIGHT - Create a Procfile

        1: Create a Procfile at the top level of the directory.

        2: Within this file, declare the below command. This command ensures gunicorn is used as the web server.

            web: gunicorn restobook.wsgi
        
        *Add, commit and push to the repository at this point*
    
    ---
    
    * STAGE NINE - Connect the GitHub repository to the Heroku App

        1: Within the Deploy tab on the Heroku app, choose GitHub as the deployment method.

        2: Search for the correct repository and connect.

        3: At the bottom of the deployment section there is an option to chose which branch to deploy. Chose the main branch and allow the build log to complete.

        4: Once complete, chose to allow automatic deployment from here onwards.

        *The app has now been deployed successfully. The live link can be found [here](https://sweet-shop-lewiscm.herokuapp.com/)*

        **Be aware, from this point onwards, all changes made to the database in development will have to be migrated to the deployed database separately in order to take effect. This can be done by changing the DATABASES dictionary in the settings.py file to point directly at the heroku database, DO NOT commit to GitHub with this setting saved.**

    ---
[Return to Table of Contents](#contents)
___

## Create a Local Clone <a name ='clone'></a>

- Follow the steps below in order to create a local clone using HTTPS.

    * STEP ONE - Navigate to the GitHub repository for the project. Located [here](https://github.com/LewisCM14/sweet-shop).
    
    * STEP TWO - From the tabs displayed, click the **Code** tab. This presents a drop down menu.

    * STEP THREE - Ensure this menu is on the **HTTPS** tab and copy the URL.

    * STEP FOUR - On your chosen IDE open Git Bash, Change the current working directory to the location where you want the cloned directory.
    
    * STEP FIVE - Type git clone, and then paste the URL you copied earlier.

            $ git clone https://github.com/LewisCM14/sweet-shop.git
    
    * STEP SIX - Press Enter to create your local clone.

    *If GitPod is your chosen IDE from the link above the Gitpod button can be clicked to open up the repository code on your local machine* 

[Return to Table of Contents](#contents)
___
## Technologies Used <a name ='tech'></a>

- **Languages Used**

    * HTML
    * CSS
    * JAVASCRIPT
    * PYTHON
    * MARKDOWN

- **Frameworks & Toolkits**

    * **[Django 3.2](https://www.djangoproject.com/download/).**
        * Python based web framework, used to build the application.
    
    * **[Bootstrap](https://getbootstrap.com/).**
        * A front-end open source toolkit, used across the application.
    
    * **[Font Awesome](https://fontawesome.com/).**
        * Icon set and toolkit used across the application.

- **DBMS**
    
    * **[PostgreSQL](https://www.postgresql.org/).**
        * The relational database management system used.

- **Cloud Services**

    * **[Heroku](https://id.heroku.com/login).**
        * The platform my project is deployed on.

    * **[AWS S3](https://aws.amazon.com/s3/).**
        * A cloud-based storage service. Used to store my static files in deployment.

- **Email Backend**

    * **[Gmail](https://mail.google.com).**
        * Mail provider used as the smtp host for email backend.

- **Server**

    * **[Gunicorn](https://gunicorn.org/).**
        * The server used to run Django on Heroku.

- **Version Control**
    
    * **Git.**
        * Git was used for version control by utilizing the GitPod terminal to commit to Git and Push to GitHub.

    * **[GitHub](https://github.com/).**
        * GitHub is used to store the projects code after being pushed from Git.
    
    * **[Gitpod](https://www.gitpod.io/docs/).**
        * The IDE used to build the project.

- **Libraries, Packages and Applications**

    * **[dj_database_url](https://pypi.org/project/dj-database-url/).**
        * A PostgreSQL supporting library. Allows you to utilize the 12factor inspired DATABASE_URL environment variable to configure your Django application.
    
    * **[pyscopg2-binary](https://www.psycopg.org/docs/).**
        * PostgreSQL database adapter for the Python programming language.    
    
    * **[allauth](https://django-allauth.readthedocs.io/en/latest/installation.html).**
        * Used for creation and maintenance of user accounts.
    
    * **[django-storage](https://django-storages.readthedocs.io/en/latest/).**
        * Built upon with boto3 to help facilitate the storage of static and media files on AWS S3.

    * **[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).**
        * Used to help facilitate the storage of static and media files on AWS S3.
    
    * **[crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/index.html).**
        * Used for rendering forms.
    
    * **[coverage](https://coverage.readthedocs.io/en/6.3/).**
        * Used to access the coverage of my automated tests for python code.
     
- **Programs**

    * **Slack.**
        * Specifically the peer-code_review channel on Code Institutes Slack workspace. Used to increase the scope of my testing.
    
    * **Balsamiq.** 
        * Used to create the wire frames during the development process.

    * **[Iconifier](https://iconifier.net/).**
        * Used to convert the favicon image to the correct size and file type.
       
[Return to Table of Contents](#contents)
___
## Credits <a name = 'credits'></a> 

* A special thank you to my mentor Rohit Sharma. 

* Thanks to the Code Institute tutor support team, who helped me develop my understanding throughout this project.

* Finally thanks to my peers on Slack who responded to my questions.  

- **Content**

- **Media**

[Return to Table of Contents](#contents)
___