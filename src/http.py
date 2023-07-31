import requests
import yaml

from src import config

with open('config.yaml', 'r', encoding='UTF-8') as cf:
    API_TOKEN = yaml.safe_load(cf)["api"]["token"]


def send_request(name, target):
    response = requests.post(
        "https://swissmodel.expasy.org/automodel",
        headers={
            "Authorization": f"Token {API_TOKEN}"
        },
        json={
            "target_sequences": target,
            "project_title": name
        }
    )
    return response


def check_status(project_id):
    response = requests.get(
        f"https://swissmodel.expasy.org/project/{project_id}/models/summary/",
        headers={
            "Authorization": f"Token {API_TOKEN}"
        }
    )
    return response


def fetch_all_projects():
    response = requests.get(
        "https://swissmodel.expasy.org/projects/",
        headers={
            "Authorization": f"Token {API_TOKEN}"
        }
    )
    return response
