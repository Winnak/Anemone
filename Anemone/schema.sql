DROP TABLE IF EXISTS configuration;
CREATE TABLE configuration (
    projectname TEXT,
    projectpath TEXT,
    unitypath TEXT,
    gitpath TEXT,
    privatessh TEXT,
    publicssh TEXT
);

DROP TABLE IF EXISTS projects;
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

DROP TABLE IF EXISTS jobs;
CREATE TABLE jobs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project INTEGER NOT NULL, -- foreign key
  status INTEGER NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  started DATETIME,
  ended DATETIME,

  FOREIGN KEY(project) REFERENCES projects(id)
);
-- Status codes:
-- 0 = none
-- 1 = succesful
-- 2 = warnings
-- 3 = errors
-- 4 = running
-- 5 = scheduled


-- temp data trash
INSERT INTO projects VALUES(0, "TestProject", "This is a test project meant for testing");
INSERT INTO jobs VALUES(0, 0, 1, 'ClearChimpanzee-001', "", datetime('2013-10-07 08:23:19.120'), datetime('2013-10-07 09:23:19.120'));
INSERT INTO jobs VALUES(1, 0, 2, 'MissionHorse-002', "",    datetime('2013-10-08 08:23:19.120'), datetime('2013-10-08 09:23:28.120'));
INSERT INTO jobs VALUES(2, 0, 3, 'MiddlePorcupine-003', "", datetime('2015-10-09 02:23:19.120'), datetime('2015-11-16 19:23:28.120'));
INSERT INTO jobs VALUES(3, 0, 4, 'OpeningBadger-004', "",   datetime('now'), null);
INSERT INTO jobs VALUES(4, 0, 5, 'ClassicVixen-005', "",    datetime('now', '+1 day'), null);
INSERT INTO jobs VALUES(5, 0, 0, 'VariousMoose-006', "",    null, null);
