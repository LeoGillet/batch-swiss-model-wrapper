"""
Module containing all requests used throughout the program
"""
import requests
import yaml

with open("config.yaml", "r", encoding="UTF-8") as cf:
    API_TOKEN = yaml.safe_load(cf)["api"]["token"]


def send_request(name, target):
    """
    Sends POST request to initiate an AutoModel job
    :param name: name of the project
    :param target: sequence to be used
    :return: JSON Response {"project_id", "target_sequences", "date_created", "project_title"}
    """
    response = requests.post(
        "https://swissmodel.expasy.org/automodel",
        headers={"Authorization": f"Token {API_TOKEN}"},
        json={"target_sequences": target, "project_title": name},
        timeout=10,
    )
    return response


def check_status(project_id):
    """
    Checks whether the Job is completed or not via a GET request
    :param project_id: ID of the project
    :return: JSON Response
    {"project_id", "status", "models", "date_created", "project_title", "view_url"}
    """
    response = requests.get(
        f"https://swissmodel.expasy.org/project/{project_id}/models/summary/",
        headers={"Authorization": f"Token {API_TOKEN}"},
        timeout=10,
    )
    return response


def fetch_all_projects():
    """
    GET Request to get a list of all projects
    :return: JSON Response
    [{"project_id", "status", "date_created", "project_title", "project_type", "model_count"}, ...]
    """
    response = requests.get(
        "https://swissmodel.expasy.org/projects/",
        headers={"Authorization": f"Token {API_TOKEN}"},
        timeout=10,
    )
    return response

def model_summary(project_id):
    """
    Sends a GET request to get models information summary about project
    """
    response = requests.get(
        f"https://swissmodel.expasy.org/project/{project_id}/models/summary/",
        headers={"Authorization": f"Token {API_TOKEN}"},
        timeout=10,
    )
    return response

def download_all() -> dict:
    """
    Sends a POST request in order to generate an archive of all completed jobs' results
    """
    response = requests.post(
        "https://swissmodel.expasy.org/projects/download/",
        headers={"Authorization": f"Token {API_TOKEN}"},
        json={
            "from_datetime": "2023-07-28T16:22:41",
            "to_datetime": "2023-07-28T16:22:43",
        },
        timeout=30,
    )
    return response.json()


def get_download_url(download_id):
    response = requests.get(
        f"https://swissmodel.expasy.org/projects/download/{download_id}",
        headers={"Authorization": f"Token {API_TOKEN}"},
        timeout=10,
    )
    return response.json()


def download(url):
    response = requests.get(url, allow_redirects=True, headers={
        "Authorization": f"Token {API_TOKEN}"
    },
    timeout=30)
    return response.content