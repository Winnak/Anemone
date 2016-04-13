# Anemone
License: [MIT](LICENSE)

![alt text](https://raw.githubusercontent.com/Winnak/Anemone/master/screenshots/Screenshot_1.png "WIP")


## Dependencies
* [https://github.com/pallets/flask](flask)
* [https://github.com/coleifer/peewee](peewee)


## Quick start guide
1. copy `Anemone_Build.cs` to your unity project Asset/Editor folder (create one if you don't have one)
2. Configure `application.cfg` to your needs
3. Run `createdatabase.py` to create the database
4. Run `runserver.py` to start the server

[application.cfg](application.cfg) change default login info and the file path to the unity installation etc.


## TODO/Roadmap
1. Build file
    * Use build file
2. Layout
    * Fix the full height sidebar
    * use timeago.js
    * Re-colorize/stylize
    * remove temp code
    * Show project health on dashboard (and maybe on project overview as well)
3. Git handling
    * ssh-key handling
    * Configurable polling / build scheduling
4. Documentation
    * Add copyright header
    * Add module information
    * Update project description
    * Create wiki?
5. User management
    * create user
    * user roles
6. Create better startup first-time stuff
    * automatically createdatabase.py if database is not there
    * create admin user on first run
7. ABC format update
    * Move the ABC format to its own repository
    * Add multiline setting
    * Internal references
    * Wildcards for datetime and other fun things?
8. Figure out solution for cloud building
    * Test using raspberry pis
9. Parse unity log file and make it more informative.
10. Perforce handling
11. Unreal Engine support?
12. SVN handling?
