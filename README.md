# Anemone
License: [MIT](LICENSE)

![alt text](https://raw.githubusercontent.com/Winnak/Anemone/master/screenshots/Screenshot_1.png "WIP")


## Dependencies
* [https://github.com/pallets/flask](flask)
* [https://github.com/coleifer/peewee](peewee)


## Quick start guide
1. copy `Anemone_Build.cs` to your unity project Asset/Editor folder (create one if you don't have one)
2. Run `createdatabase.py` to create the database
3. Run `runserver.py` to start the server

[Anemone/config.py](Anemone/config.py) change default login info


## TODO
1. Build file
    * Create CSharp reader
    * Add options
    * Add configuration view (should only read from the file and be able to target a new)
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
7. Figure out solution for cloud building
8. Parse unity log file and make it more informative.
9. Perforce handling
10. SVN handling?
