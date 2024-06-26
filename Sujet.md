# M1-CTO TP

## Using FastAPI

Ensure your code is well-commented, explaining the rationale behind your decisions.

### Setting Up FastAPI and Basic Endpoint

- **Installing dependencies and setting up the project.**
- **Creating the basic FastAPI application.**
- **Implement the `/` endpoint** that returns an HTML document with the given `name` parameter. The `index` should return a proper HTML document with the following content in the body and status code 200:

```html
<h1>Hello <span>{name}</span></h1>
```
Where `name` (without the curly braces `{}`) is a parameter given in the URL like `/arnaud`. Here, `arnaud` would be used in the HTML to say hello.

### Defining Pydantic Models

- **Creating the `Student` and `Grade` models with validation.**
  - A student should have an identifier (`UUID`), `first_name`, `last_name`, `email`, `grades`.
  - `email` should be a valid email.
  - `grades` is a list of the Pydantic model `Grade` with an identifier (`UUID`), `course` as a string, and a `score` in that course being a number between 0 and 100.

### Implementing the POST `/student` Endpoint

- **Handling JSON payloads sent as the body and save the student data.**
- **Returning the identifier of the newly created student.**

### Implementing the GET `/student/{identifier}` Endpoint

- **Retrieving the student data by identifier using the previously created student id.**
- **Returning the student data in JSON format.**

### Implementing the DELETE `/student/{identifier}` Endpoint

- **Handling deletion of student data.**
- **Ensuring subsequent requests to the deleted identifier return a 404 status.**

### Implementing the GET `/student/{identifier}/grades/{identifier}` Endpoint

- **Retrieving a specific grade for a student.**
- **Returning the grade data in JSON format.**

### Implementing the DELETE `/student/{identifier}/grades/{identifier}` Endpoint

- **Handling deletion of a specific grade for a student.**
- **Ensuring subsequent requests to the deleted grade return a 404 status.**

### Creating the `/export` Endpoint

- **Handling the request to export data in JSON or CSV format.**
- **Defaulting to CSV if no format is specified.**

### Bonus: Testing and Debugging

- **Testing all endpoints to ensure they work as expected using pytest, for example.**
- **Provide a command or explanations on how to run the tests.**
- **Debugging any issues that arise.**

### Bonus: Implement Authentication and Protect the POST Routes

- **It should accept a username and password using Basic authentication.**