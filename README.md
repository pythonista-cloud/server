# pythonista.cloud Server [![Build Status](https://travis-ci.org/pythonista-cloud/server.svg?branch=master)](https://travis-ci.org/pythonista-cloud/server) [![Coverage Status](https://coveralls.io/repos/github/pythonista-cloud/server/badge.svg?branch=master)](https://coveralls.io/github/pythonista-cloud/server?branch=master)

This package manages the index of modules. Most of the heavy lifting is done by [`CouchDB`](https://couchdb.apache.org), but the server still contains:
- Code for submitting packages
- A Python script that enforces the structure of packages as they are submitted.

### Package structure
Packages are represented as JSON. The following fields are supported in your module's JSON file:
- `name` (required) - the name of your module
- `url` (required) - a link pointing to the GitHub repo where your module lives
- `entry_point` (required) - the path inside your GitHub repo where your package actually lives. This should point to your main `.py` file if you have a single-file module, and to your package directory if you have a multi-file package.
- `py_versions` - either `[2]`, `[3]`, or `[2, 3]` depending on which major Python versions your module supports
