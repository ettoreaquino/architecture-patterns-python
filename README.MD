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

## Chapter 03 - Abstractions
Since this chapter is just an interlude, we shall not sincronize it with the master branch. Thus, in order to acess it:

```git checkout ch-03-abstractions```

## Chapter 04 - Service Layer
In this chapter the authors add a Service Layer, which will be called using Flask. This Layer will work as an entrypoint for our domain model.
Because the service layer depends on the AbstractRepository, we can unit test it by using FakeRepository but run our production code using SqlAlchemyRepository.

<img src=images/ch4_serviceLayer.png
     alt="serviceLayer Icon" />

At this point we will need to spin up containers, so that we can test the application against a proper DB as well as provide an endpoint for our API to be called.

My choice here was to refactor the infrastructure to use Falcon instead of Flask, as well as use Poetry to manage the dependencies.

Even though our architeture is taking shape the service layer is still tightly coupled to the domain, because its API is expressed in terms of OrderLine objects. This will be corrected further down the road.

Here is where we are so far:

<img src=images/ch4_serviceLayerArchitecture.png
     alt="serviceLayer Architecture Icon" />

## Chapter 05 - TDD in High Gear and Low Gear

Since we can test our software against the service layer, we don’t really need tests for the domain model anymore. Instead, we could rewrite all of the domain-level tests in terms of the service layer.

The idea behind this chapter is to bring awareness to at which level of abstraction should you write your codes, and that is why you should decouple the tests for your domain services. This will allow you to test against your services whenever you need to reflect about a new feature that does not need a domain model refactoring.

In order to do that, we shall have a service layer that's fully decoupled from the domain, we need to rewrite its API to work in terms of primitives.