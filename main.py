from src import http, config, parser, job


if __name__ == '__main__':
    # CFG = config.parse_config()
    sequences = parser.read_fasta()
    jobs = job.create_jobs_from_sequences(sequences)
    job_count = len(jobs)
    existing_projects = [project['project_title'] for project in http.fetch_all_projects().json()]
    jobs = [job for job in jobs if job.name not in existing_projects]
    if False:
        job.submit_all_jobs(jobs)
        print(f"Submitted {job_count} jobs.")
        job.refresh_all_jobs(jobs)
        while True:
            jobs_done = job.count_all_jobs_done(jobs)
            if jobs_done == job_count:
                break
            print(f"{jobs_done}/{job_count} jobs completed. Waiting 10 seconds...")
            job.refresh_all_jobs(jobs)
