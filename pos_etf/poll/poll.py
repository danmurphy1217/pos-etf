from __future__ import annotations
from typing import Callable, Optional, List
import datetime
import time


class Poll:

    def __init__(self, job_name: str, job_description: str):
        """Each instance of Poll should have a job name and description"""
        self.job_name = job_name
        self.job_description = job_description
        self.jobs: List[Task] = []

    def every(self, min_interval: int) -> Task:
        """
        Create a new poller at every ``interval`` minutes.

        :param self -> ``Poll``:
        :param min_interval -> ``int``: interval of minutes to run the poll.

        :returns -> ``Task``: a newly instantiated Task object containing the minute interval and a reference
                              to the Poll object.
        """
        task = Task(min_interval, self)

        return task

    def run_all(self):
        """Run all jobs in self.jobs"""
        for job in self.jobs:
            result = job.task_func()
            print(result)

    def run_pending(self):
        """Run pending jobs in self.jobs"""
        # filter jobs
        runnable_jobs = filter(lambda job: job._should_run(), self.jobs)
        # run those that meet criteria for pending
        for job in runnable_jobs:
            result = job.task_func()
            print(result)

    def run(self):
        """Run the last job in self.poller.jobs (the job bound to the class instance), return the result."""
        assert self.task_func == self.jobs[-1].task_func, "The last Task added to self.poller.jobs must be the task bound to the currently invoked class."
        task_res = self.task_func()
        return task_res


class Task:

    def __init__(self, min_interval: int, poller: Poll = None):
        """
        Each task object should be instantiated with the minute interval
        and a reference to the Poll object from which it is returned.
        """

        self.min_interval = min_interval
        self.poller: Optional[Poll] = poller
        self.next_run: Optional[datetime.datetime] = None

    def _should_run(self):
        """
        checks if a job should run (current time is greater than or equal to the next run of the task)
        """
        return datetime.datetine.now() >= self.next_run

    def _schedule_next_run(self):
        """
        schedule the next run for a task.
        """

        timedelta_interval = datetime.timedelta(
            **{"minutes": self.min_interval})
        print(timedelta_interval)
        self.next_run = datetime.datetime.now() + timedelta_interval
        print(self.next_run)
        return self.next_run

    def do(self, func: Callable) -> Task:
        """
        define the job to be run at each interval.

        :param func -> ``Callable``: the function to run at each interval.

        :return -> ``Task``: modified task upject with the next run scheduled and the task added to the scheduler.
        """
        self.task_func = func
        self._schedule_next_run()

        # add the Task object to self.poller.jobs
        self.poller.jobs.append(self)

        return self

    def run(self):
        """Run the last job in self.poller.jobs (the job bound to the class instance), return the result."""
        assert self.task_func == self.poller.jobs[-1].task_func, "The last Task added to self.poller.jobs must be the task bound to the currently invoked class."
        task_res = self.task_func()
        return task_res

    def run_all(self):
        """API for running all jobs immediately after defining a task"""
        for job in self.poller.jobs:
            print(job())

    def run_pending(self):
        """API for running pending jobs immediately after defining a task"""
        # filter jobs
        # run those that meet criteria for pending
        runnable_jobs = filter(lambda job: job._should_run(), self.poller.jobs)
        print(runnable_jobs)


def tester():
    return list("Yo")


def test_two():
    return ["1", "2"]


poll = Poll("Test", "This is a test description")

poll.every(10).do(test_two)
poll.every(5).do(tester)
poll.every(5).do(tester)

while True:
    poll.run_all()
    time.sleep(1)


# poll.every(num_of_minutes).do(func_to_do)
# poll.run_pending() -> run any pending tasks
# poll.run_all() -> run all regardless
# poll.run() -> run most recent task
# update _schedule_next_round() to make sure timing interval actually works.