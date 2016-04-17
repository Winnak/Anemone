# Anemone
License: [MIT](LICENSE)

![alt text](https://raw.githubusercontent.com/Winnak/Anemone/master/screenshots/Screenshot_1.png "WIP")


## Dependencies
* [https://github.com/pallets/flask](flask)
* [https://github.com/coleifer/peewee](peewee)


## Quick start guide
1. copy `AnemoneBuild.cs` to your unity project Asset/Editor folder (create one if you don't have one)
2. copy `build.abc` to your unity project's root folder, configure as you see fit.
3. Configure `application.cfg` to your needs
4. Run `createdatabase.py` to create the database
5. Run `runserver.py` to start the server

[application.cfg](application.cfg) change default login info and the file path to the unity installation etc.


## TODO/Roadmap
0. Layout
    * use timeago.js
1. Jobs
    * Fix status
    * Pipe log
    * Schedule a job
    * More actions
2. Git handling
    * ssh-key handling
    * Configurable polling / build scheduling
3. Documentation
    * Add copyright header
    * Add module information
    * Update project description
    * Create wiki?
4. User management
    * create user
    * user roles
5. Create better startup first-time stuff
    * GUI for configuring application.cfg
    * automatically createdatabase.py if database is not there
    * build file wizard
    * create admin user on first run
6. ABC format update
    * Move the ABC format to its own repository
    * Add multiline setting
    * Internal references
    * Wildcards for datetime and other fun things?
7. Figure out solution for cloud building
    * Test using raspberry pis
8. Layout
    * Fix the full height sidebar or figure out a new, more modern layout
    * Re-colorize/stylize
9. Parse unity log file and make it more informative.
10. Perforce handling
11. Unreal Engine support?
12. SVN handling?
