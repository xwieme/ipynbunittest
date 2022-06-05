# Ipynbunittest

Ipynbunittest is a python module that can run pytest in ipython notebooks where the tests are 
defined in a separate python file.

## Requirements

| Module | version |
| --- | --- |
| pytest | 7 |
| ipykernel | 6.13.0|

## Functions

### `run_unit_test(test_filepath, notebook)`

Run one unit test in a jupyter notebook. The function requires a path to a pytest test class and the
filename of the current notebook. The following example shows how functions that are defined in the 
jupyter notebook can be used in the test class.

e.g.: if the test file is called test_A.py the following import statement is used to access functions in the jupyter notebook
~~~python
from A import *
~~~

### `run_unit_tests(test_filepaths, notebook)`

Run multiple unit tests in a jupyter notebook.

### `all(path)`

Test all notebooks that have a corresponding test file, where the test filename is assumed to be the 
same as the notebook filename with the prefix test_ and located in the folder ./tests.