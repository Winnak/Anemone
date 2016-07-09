# Anemone
License: [MIT](LICENSE)

![Screenshot_1](https://raw.githubusercontent.com/Winnak/Anemone/master/screenshots/Screenshot_1.png "WIP")


## Dependencies
* [https://github.com/pallets/flask](flask)
* [https://github.com/coleifer/peewee](peewee)
* [https://github.com/agronholm/apscheduler](APScheduler)
* [https://github.com/gitpython-developers/GitPython](GitPython)


## Quick start guide
1. copy `build.abc` to your unity project's root folder, configure as you see fit.
2. Configure `application.cfg` to your needs (make sure it points to your ssh key)
3. Run `createdatabase.py` to create the database
4. Run `runserver.py` to start the server

[application.cfg](application.cfg) change default login info and the file path to the unity installation etc.

Make sure that your ssh key is not password protected, as it is not supported yet.

## TODO/Roadmap
1. User management
    * create user.
    * user roles.
2. Documentation
    * Add copyright header.
    * Add module information.
    * Update project description.
    * Create wiki?
    * setup.py script?
3. Figure out solution for cloud building
    * Pairing.
    * Ordering.
    * Test using raspberry pi.
4. Advanced scheduling
    * Integrate APScheduler into current database.
    * Configurable polling rate.
    * Restart unrunned jobs.
    * Make a special build every morning (with toggle "iff repo change")
    * More actions.
5. Create better startup first-time stuff
    * create admin user on first run.
    * GUI for configuring application.cfg.
    * automatically createdatabase.py if database is not there.
    * build file wizard.
    * Setup SSH key
6. Layout
    * Create view for retrieving the output files.
    * Fix the full height sidebar or figure out a new, more modern layout.
    * Redo health display
    * Re-colorize/stylize.
7. Parse unity log file and make it more informative.
8. Look into long polling for live updating website.
9. Perforce handling.
10. SVN handling?
11. Unreal Engine support?
