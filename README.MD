# ARCHITECTURE PATTERN IN PYTHON
This is a repository to hold tests and developments based on the book:

Architecture Patterns with Python

## Chapter 01 - Domain Modelling
This chapters applies a TDD approach to validate a Domain Model, note that there is no project structure yet.

`src/model.py` Holds **Entities** and **Value Objects**, while `src/services.py` holds **Domain Services**. 

The tests are ALWAYS developed prior to the implementation of the entities, value objects and services. Once developed you will have a better visualization of how you objects and methods should work to validate your model.

1. Develop Test
2. Develop the Entities, Value Objects and Services necessary to validate that Test
3. Perform the test:

```make test``` 

Repeat the process as your domain evolves.

## Chapter 02 - Repository Pattern

The key here is to make sure your repository depends on the model, and not the other way around. *Dependency Inversion Principle*

The use of ORM or not (writing the database integrations yourself) is a point of heavy debate. For the sake of this tutorial the main objective is to properly implement the DDD principles using Python. The fact that we are using an ORM does not hurt the Dependency Inversion Principle.

We also made sure to extend and Absstract Class when implementing the Repository object. Which allows us to mock respositories for tests very quickly. 

