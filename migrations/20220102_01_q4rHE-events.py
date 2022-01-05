"""
events
"""

from yoyo import step

__depends__ = {"20211226_01_zx3oY-forge-data"}

steps = [
    step(
        """
        --- tasks scheduled by remote Interfaces
        CREATE TABLE IF NOT EXISTS remote_tasks(
            ID INTEGER PRIMARY KEY NOT NULL,
            job_id VARCHAR(36) NOT NULL,
            signed_by INTEGER REFERENCES interfaces(ID) ON DELETE CASCADE NOT NULL,
            ---  Different values for status:
            ---     0 = queued
            ---     1 = completed
            ---     -1 = error
            status INTEGER NOT NULL DEFAULT 0,
            created VARCHAR(40) NOT NULL,
            updated VARCHAR(40) DEFAULT NULL,
            UNIQUE(job_id, signed_by)
        );
    """
    ),
    step(
        """
        --- tasks scheduled by remote Interfaces
        CREATE TABLE IF NOT EXISTS remote_tasks_json(
            ID INTEGER PRIMARY KEY NOT NULL,
            task_id UNIQUE REFERENCES tasks(ID) ON DELETE CASCADE NOT NULL,
            json TEXT NOT NULL
        );
    """
    ),
    step(
        """
        --- tasks scheduled by local Interfaces
        CREATE TABLE IF NOT EXISTS local_tasks(
            ID INTEGER PRIMARY KEY NOT NULL,
            job_id VARCHAR(36) NOT NULL,
            signed_by INTEGER REFERENCES interfaces(ID) ON DELETE CASCADE NOT NULL,
            ---  Different values for status:
            ---     0 = queued
            ---     1 = completed
            ---     -1 = error
            status INTEGER NOT NULL DEFAULT 0,
            created VARCHAR(40) NOT NULL,
            updated VARCHAR(40) DEFAULT NULL,
            UNIQUE(job_id, signed_by)
        );
    """
    ),
    step(
        """
        --- tasks scheduled by local Interfaces
        CREATE TABLE IF NOT EXISTS local_tasks_json(
            ID INTEGER PRIMARY KEY NOT NULL,
            task_id UNIQUE REFERENCES tasks(ID) ON DELETE CASCADE NOT NULL,
            json TEXT NOT NULL
        );
    """
    ),
]
