"""
Entry point of the program
"""
from src import http, parser, job


if __name__ == "__main__":
    # CFG = config.parse_config()
    sequences = parser.read_fasta()
    jobs = job.create_jobs_from_sequences(sequences)
    us = parser.unique_sequences_stats(sequences)
    parser.export_unique_sequences_fasta(us)
    while True:
        existing_projects = [
            project["project_title"] for project in http.fetch_all_projects().json()
        ]
        jobs = [job for job in jobs if job.name not in existing_projects]
        job_count = len(jobs)
        if job_count == 0:
            break
        print(f"Submitting {job_count} jobs.")
        job.submit_all_jobs(jobs)
    job.refresh_all_jobs(jobs)
    while True:
        JOBS_DONE = job.count_all_jobs_done(jobs)
        if JOBS_DONE == job_count:
            break
        print(f"{JOBS_DONE}/{job_count} jobs completed. Waiting 10 seconds...")
        job.refresh_all_jobs(jobs)
