"""
Classes and functions for the creation and processing of jobs
"""
import time
import threading

from src import http


class Job:
    """
    Job/Project class
    """

    def __init__(self, name, sequence):
        self.name: str = "batch_" + name
        self.sequence: str = sequence
        self.status: str = "NOT SUBMITTED"
        self._first_response = None
        self.project_id = None
        self._last_status_response = None
        self.models = []

    def submit_task(self):
        """
        Submits job via POST request to Swiss-Model API
        """
        self._first_response = http.send_request(self.name, self.sequence)
        try:
            self.project_id = self._first_response.json()["project_id"]
            print(self._first_response.json())
            if self._first_response.status_code == 429: raise RuntimeError
        except (KeyError, TypeError, RuntimeError):
            print(f"Job {self.name}: Rate limit exceeded.")
            time.sleep(60)        
        else:
            print(f"Job {self.name} status: {self.status} -> SUBMITTED") 
            self.status = "SUBMITTED"

    def update_status(self):
        """
        Sends GET request to API and updates status of job
        """
        if not self.project_id or self.status == "NOT SUBMITTED":
            raise RuntimeError(
                f"Cannot check status of Job {self.name} because it has not yet been submitted."
            )
        if self.status == "COMPLETED": return self.fetch_results()
        self._last_status_response = http.check_status(self.project_id)
        print(f"Job {self.name} status: {self.status} -> {self._last_status_response.json()['status']}") 
        self.status = self._last_status_response.json()["status"]

    def fetch_results(self):
        """
        Fetches models of completed job
        """
        if self.status not in ("COMPLETED", "FAILED"):
            raise RuntimeError(f"Cannot fetch results of Job {self.name} that has not finished.")
        if self.status == "FAILED":
            raise RuntimeError(f"Job {self.name} has failed. Stopping.")
        if self.status == "COMPLETED":
            models = self._last_status_response.json()["models"]
            self.models = [model["coordinates_url"] for model in models]

    def __str__(self):
        return f"Job: {self.name} {len(self.sequence)} aa."


def create_jobs_from_sequences(sequences: list[tuple[str, str]], debug=None):
    """
    Given a FASTA input, creates a job with name and sequence
    :param sequences: list containing pairs of sequences name and sequence
    :param debug: limits number of jobs created and in returned list
    :return: List of jobs
    """
    if debug and isinstance(debug, int) and debug < len(sequences):
        return [Job(name, seq) for name, seq in sequences[:debug]]
    return [Job(name, seq) for name, seq in sequences]


def submit_all_jobs(jobs):
    """
    Submits all jobs in given list
    :param jobs: jobs
    """
    submit_threads = []
    job_count = len(jobs)
    for i, job in enumerate(jobs):
        print(f"[{i+1}/{job_count}] Job {job.name}: submitting task...")
        thread = threading.Thread(target=job.submit_task)
        thread.start()
        submit_threads.append(thread)
        time.sleep(1)

    for thread in submit_threads:
        thread.join()


def refresh_all_jobs(jobs, sleep=10):
    """
    Requests API in order to refresh job's status
    :param jobs: jobs
    :param sleep: time sleeping after request
    """
    refresh_threads = []
    job_count = len(jobs)
    for i, job in enumerate(jobs):
        print(f"[{i+1}/{job_count}] Job {job.name}: refreshing status...")
        thread = threading.Thread(target=job.update_status)
        thread.start()
        refresh_threads.append(thread)
        time.sleep(1)

    for thread in refresh_threads:
        thread.join()

    if sleep and isinstance(sleep, int):
        time.sleep(sleep)


def count_all_jobs_done(jobs):
    """
    Counts all jobs that are either successfully completed or have failed
    :param jobs: jobs
    :return: number of completed jobs
    """
    count = 0
    for job in jobs:
        if job.status in ("COMPLETED", "FAILED"):
            count += 1
    return count
