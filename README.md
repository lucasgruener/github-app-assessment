# github-app

- The app will retrieve an user most recent public repositories on github and display it.

- The app will also save the information about the user and the repositories in an SQL database.

- If the user information is already available in the database the call to the github API will be skipped and an SQL query is done in the database.

- A worker service will keep the data on the database being updated to prevent it from getting stale.

Intructions on how to run each service are specified on the respective README.md file of the service folder
