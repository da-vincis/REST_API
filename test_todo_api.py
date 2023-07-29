import requests  # the requests library lets to interact with HTTP directly in Python
import pytest  # This import statement is a quick way to find out whether the pytest actually installed
import uuid  # the uuid is a library which contains random unique uuids

ENDPOINT = "https://todo.pixegami.io/"  # The assigned link to the endpoint makes it easier for everytime usage of it


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)  # The first request, it gets the endpoint using already assigned ENDPOINT variable
    assert response.status_code == 200  # If the response is successful, the assertion will pass if not will fail and throw an exception
    """"
        # To get data which we see in a browser when entering the https://todo.pixegami.io/ link
        #   use the below code
        data = response.json()  # Gets the json data of the response 
        print(data)  # Prints the {"message":"Hello World from Todo API"} data 
    """


def create_task(payload):
    # Creates task
    """ The create_task function creates a task using put request
        and gets a json payload for a request as an argument """
    return requests.put(ENDPOINT + "/create-task", json=payload)


def update_task_payload(payload):
    # Updates task
    """ The update_task_payload function updates a task using put request
            and gets a json payload for a request as an argument"""
    return requests.put(ENDPOINT + "/update-task", json=payload)


def get_task(task_id):
    # Gets task
    """ The get_task function gets a task using get request
                and gets an ID of the task as an argument"""
    return requests.get(ENDPOINT + f"/get-task/{task_id}")


def list_tasks(user_id):
    # Lists task
    """ The list_tasks function gets a list of tasks of a user using get request
                    and gets a user ID as an argument"""
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")


def delete_task(task_id):
    # Deletes a task
    """ The delete_task function deletes a task using delete request
                    and gets an ID of the task as an argument"""
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")


def new_task_payload():
    # Payload for tasks
    """"The new_task_payload function generates a random hex decoded uuid
            for user_id and content and returns a json - { "content": content, "user_id": user_id, "is_done": False }"""
    user_id = f"test_user_{uuid.uuid4().hex}"  # Gets an uuid from uuid4() and represents it in hex formatting
    content = f"test_content_{uuid.uuid4().hex}"  # The same as above only for "content"

    return {
        "user_id": user_id,  # Generated random user_id
        "content": content,  # Generated random content
        "is_done": False  # Whether is done
    }


def test_can_create_task():
    """" The test_can_create_task() function creates a task,
    gets the task by using get_task(task_id) function and asserts
    whether the given unique user_id and content are stored when creating the task
    """
    payload = new_task_payload()  # Gets a specific payload which contains specific user_id, content, is_done
    create_task_response = create_task(payload)  # Creates a task using specific payload
    assert create_task_response.status_code == 200  # Asserts whether the task is created successfully

    data = create_task_response.json()  # Gets the json response of the create-task put request

    task_id = data['task']['task_id']  # Gets task_id from the response json to make get-task get request for asserting whether that task exists
    get_task_response = get_task(task_id)  # Does get request using task_id which was created and returned in the json response of the create-task put request

    assert get_task_response.status_code == 200  # Asserts whether such a task_id exists

    get_task_data = create_task_response.json()  # In this line the create_task_response.json() assigned one more time to another variable to make the script more readable
                                                    # and of course we could use the "data" variable above and do not use extra assign

    assert get_task_data['task']['content'] == payload['content']  # Asserts whether the content of the returned response of the put create-request request equals to generated content in the new_task_payload function
    assert get_task_data['task']['user_id'] == payload['user_id']  # Asserts the same as above assertion but in this case for user_id


def test_can_update_task():
    """"The test_can_update_task() creates a task, updates the task
    using the task_id which was generated when creating the task and
    asserts whether the given data is stored after the update
    """
    # crate a task
    payload = new_task_payload()  # Gets a specific payload which contains specific user_id, content, is_done
    create_task_response = create_task(payload)  # Creates a task using specific payload
    assert create_task_response.status_code == 200  # Asserts whether the task is created successfully
    task_id = create_task_response.json()['task']['task_id']  # Gets the unique task_id of the created task

    # update the task
    # the new_payload json is the payload which data will update the created task
    new_payload = {
        "user_id": payload["user_id"],  # user_id is the same which was generated when creating the task
        "task_id": task_id,  # task_id is the same which was generated when creating the task
        "content": "my updated content",  # The text which will be stored as update for the task
        "is_done": True  # is_done is true because after update we want to know whether it's done
    }
    update_task_response = update_task_payload(new_payload)  # Updates the created task
    assert update_task_response.status_code == 200  # Asserts whether the update is successful

    # get and validate changes
    get_task_response = get_task(task_id)  # Gets the updated task using the unique task_id
    assert get_task_response.status_code == 200  # Asserts whether the response code of getting the task is 200
    get_task_data = get_task_response.json()  # Gets the response json of the task
    assert get_task_data["content"] == new_payload["content"]  # Asserts whether the updated content the same which was given
    assert get_task_data["is_done"] == new_payload["is_done"]  # Asserts whether the updated is_done the same which was given


def test_can_list_task():
    """"The test_can_list_task() function lists N tasks for
    the created unique user_id
    """
    # Create N tasks
    payload = new_task_payload()  # Gets a specific payload which contains specific user_id, content, is_done
    n = 3  # n is the count of how many tasks to create for a user_id
    for _ in range(n):
        create_task_response = create_task(payload)  # Creates a task using the given payload
        assert create_task_response.status_code == 200  # Asserts whether the status code of the response is 200

    # List tasks and check that there are N items
    user_id = payload["user_id"]  # Gets the unique user_id from payload
    list_tasks_response = list_tasks(user_id)  # Lists the tasks of the specific user_id
    assert list_tasks_response.status_code == 200  # Asserts whether the status code is 200 of listing the task
    data = list_tasks_response.json()  # Gets the response json of the list-tasks request

    tasks = data["tasks"]  # Gets the tasks from the response json of the list-tasks request
    assert len(tasks) == n  # Asserts whether the length of the created tasks the same which was given


def test_can_delete_task():
    """"The test_can_delete_task() function creates a task,
        deletes the task and asserts whether the task is deleted
    """
    # Create a task
    payload = new_task_payload()  # Gets a specific payload which contains specific user_id, content, is_done
    create_task_response = create_task(payload)  # Creates a task using specific payload
    assert create_task_response.status_code == 200  # Asserts whether the status code of the response is 200
    task_id = create_task_response.json()["task"]["task_id"]  # Gets the task_id of the created task

    # Delete the task
    delete_task_response = delete_task(task_id)  # Deletes the task using the unique task_id of the task
    assert delete_task_response.status_code == 200  # Asserts whether the status code of deletion is 200

    # Get the task, and check that it's not found
    get_task_response = get_task(task_id)  # Gets the deleted task using the task_id of the task
    assert get_task_response.status_code == 404  # Asserts whether the status code is 404, it means the task can not be accessed after deletion


# Thank you for going through this project:)

# The developed full course tutorial of this project you can watch in the YouTube video, see the link below
# https://www.youtube.com/watch?v=7dgQRVqF1N0
