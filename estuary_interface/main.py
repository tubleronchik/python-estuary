#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
import json
import argparse
import typing as tp
import logging

logger = logging.getLogger("estuary_interface")
logger.propagate = False
logger.level = "INFO"


def _set_headers() -> tp.Tuple[dict]:
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


def add_cid(cid: str) -> str:
    """
    Take an existing IPFS CID, and make storage deals for it.
    """
    auth_header, json_header, form_header = _set_headers()
    data = json.dumps(
        {
            "name": f"{cid}",
            "root": f"{cid}",
        }
    )
    params = json.dumps({"ignore-dupes": "true"})
    response = requests.post(
        url="https://api.estuary.tech/content/add-ipfs",
        data=data,
        headers=json_header,
        params=params,
    )
    print(response.text)


def _get_upload_endpoints() -> tp.List[str]:
    """
    Get endpoints for uploading data
    """
    auth_header, json_header, form_header = _set_headers()
    response = requests.get("https://api.estuary.tech/viewer", headers=auth_header)
    endpoints_list = json.loads(response.text)["settings"]["uploadEndpoints"]
    return endpoints_list


def add_content(file_path: str) -> str:
    """
    Upload file to Estuary Node. One file at a time.
    """
    auth_header, json_header, form_header = _set_headers()
    body = {"data": (open(file_path, "rb"))}
    response = requests.post(
        url="https://api.estuary.tech/content/add",
        files=body,
        headers=form_header,
    )
    print(response.text)
    if "error" in json.loads(response.text).keys():
        if json.loads(response.text)["error"] == "ERR_CONTENT_ADDING_DISABLED":
            endpoints = _get_upload_endpoints()
            for link in endpoints:
                response = requests.post(
                    url=link,
                    files=body,
                    headers=form_header,
                )
                if response.status_code == 200:
                    break
                print(response.text)
        else:
            logger.warning(f"Error submitting data: {response.text}")
    print(response.text)
    if response.status_code == 200:
        return f"Data was uploaded successfully. CID is: {json.loads(response.text)['cid']}"


def run():
    global token
    parser = argparse.ArgumentParser(description="Add API token for Estuary.")
    parser.add_argument(
        "token",
        type=str,
        help="API token",
    )
    args = parser.parse_args()
    token = args.token


if __name__ == "__main__":
    run()
