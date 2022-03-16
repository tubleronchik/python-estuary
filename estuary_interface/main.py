#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request
import requests
import json
import argparse
import typing as tp


def set_headers() -> tp.Tuple[dict]:
    auth_header = {"Authorization": f"Bearer {token}"}
    json_header = {
        "Authorization": f"Bearer {token}",
        "contentType": "application/json",
    }
    form_header = {
        "Authorization": f"Bearer {token}",
        "contentType": "multipart/form-data",
    }
    return (auth_header, json_header, form_header)


def add_cid(cid: str):
    auth_header, json_header, form_header = set_headers()
    data = json.dumps(
        {
            "name": f"{cid}",
            "root": f"{cid}",
        }
    )
    response = requests.post(
        url="https://api.estuary.tech/content/add-ipfs",
        data=data,
        headers=json_header,
    )
    print(response.text)


def run():
    global token
    parser = argparse.ArgumentParser(description="Add API token for Estuary.")
    parser.add_argument("token", type=str, help="API token")
    args = parser.parse_args()
    token = args.token


if __name__ == "__main__":
    run()
