import time
from datetime import datetime
from src import http

def _date() -> str:
    return datetime.now().strftime("[%H:%M:%S]")

if __name__ == '__main__':
    projects = http.fetch_all_projects().json()
    coordinates_export_rows = []
    for i, project in enumerate(projects):
        print(f"{_date()} [{i+1}/{len(projects)}] Now fetching project {project['project_id']} with {project['model_count']} models.")
        project_summary = http.model_summary(project["project_id"]).json()
        if "models" in project_summary.keys():
            model_found = False
            if isinstance(project_summary["models"], list):
                for model in project_summary["models"]:
                    if model["status"] == 'COMPLETED' and 'qmean_global' in model.keys():
                        coordinates_export_rows.append(f"{project['project_id']},{project['project_title']},{model['coordinates_url']}\n")
                        model_found = True
                        break
                if not model_found:
                    coordinates_export_rows.append(f"{project['project_id']},{project['project_title']},no correct model found\n")
            else: 
                print(project_summary["models"])
        if "error" in project_summary.keys():
            print(f"{_date()} Exceeded rate limit. Waiting 30 seconds...")
            time.sleep(30)
    
    with open('exported_coordinates.csv', 'w', encoding='UTF-8') as coords_file:
        for line in coordinates_export_rows:
            coords_file.write(line)