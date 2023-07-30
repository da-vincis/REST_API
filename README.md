# In this project we will test REST API endpoint in Python using PyTest [![Python][python-shield]][] [![LinkedIn][linkedin-shield]][https://www.linkedin.com/in/vahagn-mesropyan-ctfl]<br />

_#All the libraries are installed in the myenv virtual environment, so actually you don't have to install anything_ <br /><br />

> -So what the API is
>
> -Basically it's an HTTP endpoint and when the request is made to it, it does something and sends a response back 
<br />
The used endpoint of this project is a to-do list application, 
it has API endpoints for creating, updating, getting and deleting an item <br /><br />
<br />

![rest_api_test](https://github.com/da-vincis/RestAPI/assets/139674525/b3a7eb38-ee69-471d-a74e-167f165c5f67)


_The link of the API docs is `https://todo.pixegami.io/docs`_<br />

**The schedule is:**
1. Make requests to the API endpoints for creating, updating, getting and deleting an item
2. Assert responses
3. Develop an automated test suite in Python using PyTest framework
4. Run the tests and test suites using features of the PyTest <br /><br />

> _The developed script with the comments is available in the test_to_do.py file in the same repository_ <br /><br />

**Use the following commands to run tests:**

- To run all the files in the project which are test(those are starting with test_ name) use the following command: `pytest -m`
- To see more details about the test add the v flag: `pytest -m -v`
- To run only the specific test use the following command: `pytest -v -s .\test_todo_api.py::name_of_the_test` (Example: `pytest -v -s .\test_todo_api.py::test_can_delete_task`) <br /><br />
> _If you get the "The term 'pytest' is not recognized..." error use the following command: `python <a flag> pytest` (Example: `python -m pytest`)_<br /><br />
# Thanks for watching, I appreciate feedbacks if any <br />
