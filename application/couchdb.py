"""Utilities for working with the CouchDB used by pythonista.cloud."""
import keyword
import os
import urllib.parse

import jsonschema
import requests


# GLOBALS

COUCH_URL = "http://localhost:5984/"
MAIN_DB = "pythonista-cloud"

PACKAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "url": {"type": "string"},
        "entry_point": {"type": "string"},
        "py_versions": {
            "type": "array",
            "items": {
                "type": "integer"
            }
        },
        "name": {
            "type": "string",
            "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
        }
    },
    "required": [
        "name",
        "url",
        "entry_point"
    ]
}
PACKAGE_VALID_KEYS = PACKAGE_SCHEMA["properties"].keys()


def _add_document(doc_id, data, database=MAIN_DB):
    """Add a document to a database."""
    return requests.put(
        os.path.join(COUCH_URL, database, doc_id),
        json=data,
        headers={"Content-Type": "application/json"}
    )


def validate_package(info):
    """Verify that package JSON is valid.

    Validates:
      - Type of each key
      - That the URL is a GitHub repo
    """
    # Confirm general structure and types
    jsonschema.Draft4Validator(PACKAGE_SCHEMA).validate(info)
    url = info["url"]

    # Confirm the GitHub URL
    parts = urllib.parse.urlparse(url)
    if (parts.scheme not in ("https", "http") or
            parts.netloc not in ("github.com", "www.github.com") or
            len(parts.path.strip("/").split("/")) != 2):
        raise ValueError("That's not a GitHub repo!")
    r = requests.get(url)
    r.raise_for_status()

    # Confirm that the package name is not the name of a Python keyword
    if keyword.iskeyword(info["name"]):
        raise ValueError("Module name cannot be a Python built-in name")


def strip_package(info):
    """Remove suprerfluous keys from package JSON."""
    return {k: v for k, v in info.items() if k in PACKAGE_VALID_KEYS}


def add_package(info):
    """Add a package to the database from JSON data."""
    # Strip down the package to include only valid keys
    info = strip_package(info)

    # Infer some data and set default values
    if "py_versions" not in info:
        info["py_versions"] = [2, 3]

    # Validate the package
    validate_package(info)  # This will raise an error if anything is wrong

    # Add the package to the index, raising any errors
    _add_document(info, info["name"]).raise_for_status()
    return info
