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

In an ideal world, you’ll have all the services you need to be able to test entirely against the service layer, rather than hacking state via repositories or the database. This pays off in your end-to-end tests as well.

## Chapter 06 - Unit of Work
If the Repository pattern is our abstraction over the idea of persistent storage, the Unit of Work (UoW) pattern is our abstraction over the idea of atomic operations. It will allow us to finally and fully decouple our service layer from the data layer.

At this point a lot of communication occurs across the layers of our infrastructure: the API talks directly to the database layer to start a session, it talks to the repository layer to initialize SQLAlchemyRepository, and it talks to the service layer to ask it to allocate.

Our goal is to make the Api layer do only two things: initialize a unit of work and invoke a service. The service then, colaborate with the UoW but none of them, or the API talks directly to the database.

<img src=images/ch6_unitOfWork.png
     alt="serviceLayer Architecture Icon" />

The UoW acts as a single entrypoint to our persistent storage, and it keeps track of what objects were loaded and of the latest state.1

This gives us three useful things:

 - A stable snapshot of the database to work with, so the objects we use aren’t changing halfway through an operation

 - A way to persist all of our changes at once, so if something goes wrong, we don’t end up in an inconsistent state

 - A simple API to our persistence concerns and a handy place to get a repository.

 The Unit of Work pattern is an abstraction around data integrity
It helps to enforce the consistency of our domain model, and improves performance, by letting us perform a single flush operation at the end of an operation.

It works closely with the Repository and Service Layer patterns
The Unit of Work pattern completes our abstractions over data access by representing atomic updates. Each of our service-layer use cases runs in a single unit of work that succeeds or fails as a block.

This is a lovely case for a context manager
Context managers are an idiomatic way of defining scope in Python. We can use a context manager to automatically roll back our work at the end of a request, which means the system is safe by default.

SQLAlchemy already implements this pattern
We introduce an even simpler abstraction over the SQLAlchemy Session object in order to “narrow” the interface between the ORM and our code. This helps to keep us loosely coupled.