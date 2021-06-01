from __future__ import annotations

from typing import List, Optional
import getpass
import uuid
import os


class CronTab(object):
    """Core class object for managing existing cron jobs"""

    def __init__(self):
        self.jobs: List[CronJob] = []

    def create(self, name: str = None, description: str = None):
        """
        create a new CronJob

        :param name -> ``str``: the name of the CronJob.
        """
        name_for_job = name if name is not None else uuid.uuid4()
        desc_for_job = description if description is not None else "[No Description Provided]"

        return CronJob(name_for_job, desc_for_job, self)

    def modify(self, name: str):
        """
        modify an existing CronJob

        :param name -> ``str``: the name of the CronJob to modify.
        """

    def delete(self, name: str):
        """
        delete an existing CronJob

        :param name -> ``str``: the name of the CronJob to delete.
        """

    def write(self):
        """
        write all jobs inn
        """
        if not self.jobs[0]:
            raise Exception(
                "No Job Created. Run `CronTab().create(*args).at(*args).do(*args)` to get started.")
        else:
            user = self.jobs[0].user
            with open(f"/var/at/tabs/{user}", "w") as f:
                lines = [
                    f"{job.schedule} {job.command} # {job.name}: {job.description}\n" for job in self.jobs]
                f.writelines(lines)


class CronJob(object):
    """Class which defines a specific job"""

    def __init__(self, name: str, description: str, cron_tab: CronTab):
        self.name: str = name
        self.description: str = description
        self.cron_tab: CronTab = cron_tab

        self.user: str = getpass.getuser()
        self.schedule: Optional[str] = None
        self.command: Optional[str] = None

    def at(
        self,
        minute: Optional[int or str] = "*",
        hour: Optional[int or str] = "*",
        day: Optional[int or str] = "*",
        month: Optional[int or str] = "*",
        day_of_week: Optional[int or str] = "*"
    ) -> str:
        """
        defines the date/time at which to run the job.

        :param -> minute-> ``str``: the minute at which to run the job
        :param -> hour-> ``str``: the hour at which to run the job
        :param -> day-> ``str``: the day at which to run the job
        :param -> month-> ``str``: the month at which to run the job
        :param -> day_of_week-> ``str``: the day of week at which to run the job

        :returns -> ``str``: `self.schedule`, the date/time at which to run the job:
        """
        formatted_time_for_cron = f"{minute} {hour} {day} {month} {day_of_week}"
        self.schedule = formatted_time_for_cron
        return self

    def do(self, command: str) -> None:
        """
        defines the command to run.

        :param command -> ``str``: the command to run during job execution.

        :returns -> None:
        """
        self.command = command
        self.cron_tab.jobs.append(self)

        return self.command


ct = CronTab()
ct.create(name="Test One").at(minute="*/5").do(
    "python3 /Users/danielmurphy/Desktop/pos-etf/hi.py > /Users/danielmurphy/Desktop/this_is_test.txt")

ct.write()

#  TODO!!!
# ct.modify_job(name).at().do()
# ct.delete_job(name)
# ct.read().job(name)