# Generate-education

## Basic Requirements

- python 3.6(64 bit)
- pyenv or anaconda env
- requiremnets.txt

## Productive Requirements(include above)

- Nginx (1.15+)
- uwsgi

## Advanced Requirements(include above)

- gevent
- gunicorn

## How to run it

- source activate YOURENVNAME
- pip install -r requirement.txt
- replace the files in `PACKAGE_PATH/python3.6/site-packages/flask_images`  from flask-images with `FILE_MUST_BE_CHANGED/flask-images`
    For example : 
    My PACKAGE_PATH is `/opt/anaconda3/envs/fk/lib/python3.6/site-packages/flask_images`
- After you finished these,you can simple run it with `python run.py` to test if it really works.
- WARDING: **DO NOT** USE these in a production environments if you  only meet the **Basic Requirements**

## Architecture

### MainPage

> Included a carousel component and navbar for a convenient navigation, preview of the full content.
> Of course, you can customize the navbar and carousel via admin page.

### Module&&coursesPage

> A entrance of Generation courses,which you can learn something interesting there.
> Although it's just a demo in this repo.

### WorkingGuidancePage

> List some guidance files which make your operation more effective.
> Also,you can download them if necessary.
> From this page,you could access to the **admin page** or type it's full url .

### GenerationExperiment

> Seems that only shows some notification files for view and download.
> Actually ,I don't really know about what it use for, maybe for selecting courses later .

### AdminPage

#### Features

- User system with email verification
- File system supported videos and photos
- Content review system manually

#### Details

##### Be a member of the team

> After registeration , you need fullfill your profile . If passed you'll gain access to create your own course for students' learning .

##### Create courses

> Before creating a course . You need to prepare course name , course introduction , and an iconic photo about your course at least.
> After fundamental course information  passed , a specific course page will be created ,  you can upload the rest sections of courses there.
