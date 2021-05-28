from __future__ import annotations
from typing import Callable, Optional, List

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


class Task:
     
     def __init__(self, min_interval: int, poller: Poll = None):
         """
         Each task object should be instantiated with the minute interval 
         and a reference to the Poll object from which it is returned.
         """

         self.min_interval = min_interval
         self.poller: Optional[Poll] = poller 
    
     def do(self, poll_func: Callable) -> Task:
         """
         define the job to be run at each interval.

         :param poll_func -> ``Callable``: the function to run at each interval.

         :return -> ``Task``: modified task upject with the next run scheduled and the task added to the scheduler.
         """
         
         self.poller.jobs.append(self) # add the Task object to self.poller.jobs

         return self

def tester():
    print("Yo")

poll = Poll("Test", "This is a test description")

poll.every(5).do(tester)
poll.every(5).do(tester)
print(poll.jobs)