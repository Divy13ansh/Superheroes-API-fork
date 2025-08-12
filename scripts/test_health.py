#!/usr/bin/env python
"""
Test runner script for health app.
"""

import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def run_health_tests():
    """Run tests for the health app."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    # Run only health app tests
    failures = test_runner.run_tests(["health"])

    if failures:
        sys.exit(1)
    else:
        print("All health tests passed!")


if __name__ == "__main__":
    run_health_tests()
