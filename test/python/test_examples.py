# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test examples scripts."""

import os
import subprocess
import sys
import unittest

from qiskit.test import QiskitTestCase, online_test, slow_test

examples_dir = os.path.abspath(
    os.path.join(
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "examples"),
        "python",
    )
)
ibmq_examples_dir = os.path.join(examples_dir, "ibmq")


class TestPythonExamples(QiskitTestCase):
    """Test example scripts"""

    @unittest.skipIf(
        sys.platform == "darwin" and sys.version_info[1] >= 8,
        "Multiprocess spawn fails on macOS python >=3.8 without " "__name__ == '__main__' guard",
    )
    def test_all_examples(self):
        """Execute the example python files and pass if it returns 0."""
        examples = []
        if os.path.isdir(examples_dir):
            examples = [x for x in os.listdir(examples_dir) if x.endswith(".py")]
        for example in examples:
            with self.subTest(example=example):
                example_path = os.path.join(examples_dir, example)
                cmd = [sys.executable, example_path]
                run_example = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env={**os.environ, "PYTHONIOENCODING": "utf8"},
                )
                stdout, stderr = run_example.communicate()
                error_string = "Running example {} failed with return code {}\n".format(
                    example,
                    run_example.returncode,
                )
                error_string += f"stdout:{stdout}\nstderr: {stderr}"
                self.assertEqual(run_example.returncode, 0, error_string)

    @unittest.skipIf(
        sys.platform == "darwin" and sys.version_info[1] >= 8,
        "Multiprocess spawn fails on macOS python >=3.8 without " "__name__ == '__main__' guard",
    )
    @online_test
    @slow_test
    def test_all_ibmq_examples(self, qe_token, qe_url):
        """Execute the ibmq example python files and pass if it returns 0."""
        from qiskit import IBMQ

        IBMQ.enable_account(qe_token, qe_url)
        self.addCleanup(IBMQ.disable_account, token=qe_token, url=qe_url)
        ibmq_examples = []
        if os.path.isdir(ibmq_examples_dir):
            ibmq_examples = [x for x in os.listdir(ibmq_examples_dir) if x.endswith(".py")]
        for example in ibmq_examples:
            with self.subTest(example=example):
                example_path = os.path.join(ibmq_examples_dir, example)
                cmd = [sys.executable, example_path]
                run_example = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env={**os.environ, "PYTHONIOENCODING": "utf8"},
                )
                stdout, stderr = run_example.communicate()
                error_string = "Running example {} failed with return code {}\n".format(
                    example,
                    run_example.returncode,
                )
                error_string += f"\tstdout:{stdout}\n\tstderr: {stderr}"
                self.assertEqual(run_example.returncode, 0, error_string)
