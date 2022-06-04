import os
import json
from typing import List


def _read_notebook(filename: str) -> List[dict]:
    """
    Read a .ipynb file and returns a list containing all notebook cells

    :param filename: path to the notebook file
    """

    output = ""

    with open(filename, "r") as f:
        output = json.loads(f.read())

    return output["cells"]


def _extract_functions(cells: List[dict], out_filename) -> None:
    """
    Extract all functions from the notebook and write to file.
    Cells containing #IGNORE_TEST will be ignored.
    """

    code_file = open(out_filename, "w+")

    for cell in cells:

        if cell["cell_type"] == "code":
            content = "".join(cell["source"])

            # Check if the code cell contains the word def or an import statement
            # Also check for ignore tag
            if (
                "def" in content
                or "import" in content
                and "#IGNORE_TEST" not in content
            ):
                code_file.write(content + "\n\n\n")


def _setup_unit_test(test_filepath: str, notebook: str) -> tuple:
    """
    Setup for a unit test. Provided with a notebook file it extracts all functions and write it to a 
    file in the directory where the test file is located

    :param test_filepath: path to file where the unit test are defined
    :param notebook: name of or path to the notebook to test
    """

    assert ".py" in test_filepath, "Test file must be a python file."
    assert (
        ".ipynb" in notebook
    ), "The functions need to be defined in a jupyter notebook"

    # Get the directory of the notebook
    notebook_dir = os.getcwd()

    # Split test_filepath into a filename and a file directory
    test_filepath_parts = test_filepath.split("/")
    test_filename = test_filepath_parts[-1]
    test_filedir = "/".join(test_filepath_parts[:-1])

    # Change the working directory to the test_filedir
    os.chdir(test_filedir)

    cells = _read_notebook(f"{notebook_dir}/{notebook}")

    # Define a temporary filename where the code is written to. Use test_filename without test_
    code_filename = test_filename[5:]
    _extract_functions(cells, code_filename)

    return test_filename, code_filename, notebook_dir


def run_unit_test(
    test_filepath: str,
    notebook: str,
    skip_tests: str = None,
    clean: bool = True,
    options: str = "vx",
):
    """
    Run a unit test, using pytest, for the given notebook and test file path.

    :param test_filepath: path to file where the unit test are defined
    :param notebook: name of or path to the notebook to test
    :param skip_test: skip specific tests (default is None)
    :param clean: specify if the temporary files must be deleted (default is True)
    :param options: pytest options (default is vx meaning verbose and stop at first fail)
    """

    test_filename, code_filename, notebook_dir = _setup_unit_test(test_filepath, notebook)

    # Run pytest
    if skip_tests is None:
        os.system(f"pytest -vx {test_filename}")

    # Skip a single test
    elif isinstance(skip_tests, str):
        print(f"pytest -vxk '{test_filename[:-3]} and not {skip_tests}'")
        os.system(f"pytest -vxk '{test_filename[:-3]} and not {skip_tests}'")

    # Skip multiple tests
    elif isinstance(skip_tests, list):
        arg = " and not ".join(skip_tests)
        os.system(f"pytest -vxk '{test_filename[:-3]} {arg}'")

    # Delete the temporary file if clean is set to True
    if clean:
        os.remove(code_filename)

    # Change back to notebook directory
    os.chdir(notebook_dir)


def all(path):
    """
    Test all notebooks which are present in the directory and subdirectories that contain a corresponding 
    test file. The test filename is assumed to be the same as the corresponding notebook with the prefix
    test_

    :param path: path from where this function is called
    """

    # Change to the path from where this function is called
    os.chdir(path)

    # Get all notebooks present in the current working directory and all subdirectories
    notebooks = os.popen("find . -name *.ipynb").read().split("\n")

    # Define directory where test files are located and get a list of all test files
    test_dir = "./tests"
    test_files = os.popen("ls ./tests").read().split("\n")

    # Check for every notebook if it has corresponding test file. If it has one run pytest
    for notebook in notebooks:

        notebook_name = notebook.split("/")[-1]
        test_file = f"test_{notebook_name.split('.')[0]}.py"

        if test_file in test_files:

            _, _, notebook_dir = _setup_unit_test(f"{test_dir}/{test_file}", notebook)
                # Change back to notebook directory
            os.chdir(notebook_dir)

    # Run all unit tests in parallel
    os.system(f"pytest -x")
