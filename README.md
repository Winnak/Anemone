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
1. Project management
    * Create project
    * Soft-delete project
    * Show project health
2. Build file
    * Create simple file format (simple as in easy to implement (at least in csharp) and easy to read)
    * Create python reader
    * Create CSharp reader
    * Add options
    * Add configuration view
3. Layout
    * Fix the full height sidebar
    * Re-colorize/stylize
    * remove temp code
4. Git handling
    * ssh-key handling
    * Configurable polling
5. Documentation
    * Add copyright header
    * Update project description
    * Create wiki?
6. User management
    * create user
    * user roles
7. Create better startup first-time stuff
    * automatically createdatabase.py if database is not there
    * create admin user on first run
8. Figure out solution for cloud building
9. Parse unity log file and make it more informative.
10. Perforce handling
11. SVN handling?
