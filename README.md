# Anemone
License: [MIT](LICENSE)

![alt text](https://raw.githubusercontent.com/Winnak/Anemone/master/screenshots/Screenshot_1.png "WIP")


## Dependencies
* [https://github.com/pallets/flask](flask)
* [https://github.com/coleifer/peewee](peewee)
* [https://github.com/agronholm/apscheduler](APScheduler)


## Quick start guide
1. copy `AnemoneBuild.cs` to your unity project Asset/Editor folder (create one if you don't have one)
2. copy `build.abc` to your unity project's root folder, configure as you see fit.
3. Configure `application.cfg` to your needs
4. Run `createdatabase.py` to create the database
5. Run `runserver.py` to start the server

[application.cfg](application.cfg) change default login info and the file path to the unity installation etc.


## TODO/Roadmap
1. Jobs
    * Compress files.
2. Git handling
    * ssh-key handling.
    * Configurable polling / build scheduling.
    * Build script injection (instead of having to copy `AnemoneBuild.cs`, anemone injects it when it is time to build).
3. User management
    * create user.
    * user roles.
5. Documentation
    * Add copyright header.
    * Add module information.
    * Update project description.
    * Create wiki?
6. Figure out solution for cloud building
    * Pairing.
    * Ordering.
    * Test using raspberry pi.
7. Advanced scheduling
    * Integrate APScheduler into current database.
    * Configurable polling rate.
    * Restart unrunned jobs.
    * Make a special build every morning (with toggle "iff repo change")
    * More actions.
8. Create better startup first-time stuff
    * GUI for configuring application.cfg.
    * automatically createdatabase.py if database is not there.
    * build file wizard.
    * create admin user on first run.
9. Layout
    * Create view for retrieving the output files.
    * Fix the full height sidebar or figure out a new, more modern layout.
    * Redo health display
    * Re-colorize/stylize.
10. Parse unity log file and make it more informative.
11. Look into long polling for live updating website.
12. Perforce handling.
13. SVN handling?
14. Unreal Engine support?
