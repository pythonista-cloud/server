import unittest

import jsonschema
import requests

import application


class SubmissionTest(unittest.TestCase):
    def test_validation(self):
        # JSONSchema validation
        with self.assertRaisesRegex(jsonschema.ValidationError,
                                    "is a required property"):
            application.couchdb.add_package({})
        with self.assertRaisesRegex(jsonschema.ValidationError,
                                    "does not match"):
            application.couchdb.add_package({
                "name": "abc-def",
                "url": "https://github.com/controversial/livejson",
                "entry_point": "abcd"
            })
        with self.assertRaises(jsonschema.ValidationError):
            application.couchdb.add_package({})
        # URL validation
        with self.assertRaises(ValueError):
            application.couchdb.add_package({
                "name": "mypackage",
                "url": "https://pythonista.cloud/",
                "entry_point": "somepath.py"
            })


if __name__ == "__main__":
    unittest.main()
