import io
import os
import shutil
import zipfile

import requests
from fastapi import HTTPException


def download_github_repo_zip(
    owner: str, repo: str, branch: str = "main", dest_folder: str = "./repo"
):
    zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
    response = requests.get(zip_url)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download repository ZIP")

    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(dest_folder)

    return dest_folder
