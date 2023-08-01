import time, os

from src import http

if __name__ == '__main__':
    try:
        os.makedirs('download')
    except FileExistsError:
        pass
    with open('exported_coordinates_final.csv', 'r', encoding='UTF-8') as coords_file:
        coords = coords_file.readlines()
    for coord in coords:
        project_id, project_title, url = coord.strip().split(',')
        if not os.path.exists(f"download/{project_id}/model.pdb"):
            os.makedirs(f'download/{project_id}')
            file_content = http.download(url)
            print(f"Downloaded model {project_id}. File is {len(file_content)} bytes long.")
            with open(f'download/{project_id}/model.pdb', 'wb') as downloaded_file:
                downloaded_file.write(file_content)
            time.sleep(3)
        with open(f"download/{project_id}/info.txt", 'w', encoding='UTF-8') as infofile:
            for name in project_title.split('|'):
                infofile.write(f"{name}\n")