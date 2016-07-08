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
1. Git handling
    * Configurable polling / build scheduling.
2. User management
    * create user.
    * user roles.
3. Documentation
    * Add copyright header.
    * Add module information.
    * Update project description.
    * Create wiki?
4. Figure out solution for cloud building
    * Pairing.
    * Ordering.
    * Test using raspberry pi.
5. Advanced scheduling
    * Integrate APScheduler into current database.
    * Configurable polling rate.
    * Restart unrunned jobs.
    * Make a special build every morning (with toggle "iff repo change")
    * More actions.
6. Create better startup first-time stuff
    * create admin user on first run.
    * GUI for configuring application.cfg.
    * automatically createdatabase.py if database is not there.
    * build file wizard.
    * Setup SSH key
7. Layout
    * Create view for retrieving the output files.
    * Fix the full height sidebar or figure out a new, more modern layout.
    * Redo health display
    * Re-colorize/stylize.
8. Parse unity log file and make it more informative.
9. Look into long polling for live updating website.
10. Perforce handling.
11. SVN handling?
12. Unreal Engine support?
