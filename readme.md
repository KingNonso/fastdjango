# Fast Django - Django with FastAPI: Best of both worlds

_You might be wondering if you can use FastAPI with Django, the short answer is yes. The long answer is yes of course!!!_

Use Django as the framework and FastAPI for serving all API request purposes.

FastAPI is awesome! But lacks Django’s ecosystem, an ORM as good and well-integrated as Django’s and a Django’s admin interface.

Django is awesome but sucks at API and DRF does not even cut it.

> It’s worth noting that performance is not the only factor to consider when choosing between Django and FastAPI. In terms of raw performance, FastAPI has an edge over Django

Django is designed to handle high traffic and large-scale applications. It follows a shared-nothing architecture, allowing each component of the application to be scaled independently. Django’s caching framework supports efficient caching of database queries, views, pages, etc.

Django’s full-stack capabilities, mature ecosystem, and batteries-included approach offer significant benefits in terms of development speed, maintainability, and community support.

```
# run fastapi as stand alone on port 8000
uvicorn myapp.fastapi_old:app --reload # to load a standalone/ single instance fastapi (inside of a django app or anywhere)

# run a fastapi that talks through django as a REST API
uvicorn fastdjango.asgi:app --reload

# run GraphQL on fastapi
uvicorn fastdjango.graphql:app --reload --host 0.0.0.0 --port 8002

# run django on port 8001 - and this can be run async as well using ASGI instead of WSGI
python manage.py runserver 0.0.0.0:8001
```

## Four ways to setup

And all of that is discussed [https://sunscrapers.com/blog/fastapi-and-django-a-guide-to-elegant-integration/](https://sunscrapers.com/blog/fastapi-and-django-a-guide-to-elegant-integration/)

It however, discusses how it is run and not necessary how it is developed and interacts

This approach is the 2nd. It leverages FastAPI using Django's business logic layer. This setup leverages the strengths of both frameworks... which is ultimately our goal.

This integration facilitates the use of Django ORM's sophisticated and feature-rich models and queries within a FastAPI setting by enabling the reuse of Django project codebase.

It would make the most sense in cases where theré's need to build a fullstack application to work with data in a Panda's Dataframe using htmx or something similar.

It would also afford us to provide a lot of optimizations between the ORM and FastAPi

## Ground Rules for Prime Optimizations

1. Use Async api request
2. Use Async django db queries that means use `aget()` or `adelete()` instead of `get()` or `delete()` and when you iterate over results, you can use asynchronous iteration `(async for)` instead.
3. Use `select_related()` and `prefetch_related()` to reduce the number of database queries.
4. Use `django.db.models.query.QuerySet.as_manager()` to create a custom QuerySet manager instead of **STORED PROCEDURES**

## Why run Django and FastAPI as two separate Python Instances

The Django app is run on a separate instance to provide the Django admin which is `sync`
The FastAPI app is run on a separate instance to provide the API which is `async`
This is because Django's admin interface is not async and would not work well with async FastAPI app
But FastAPI - Django interactions are all written as async.

# BEST PRACTICE DEV TOOLS

## Use `uv` instead of `pip` for package management

uv is 8-10x faster than pip and pip-tools without caching, and 80-115x faster when running with a warm cache (e.g., recreating a virtual environment or updating a dependency).

## Use `graphql` instead of `rest` API

The adoption of GraphQL across the organisation promotes increased developer productivity and faster application shipment.
Here are proofs:

- From Paypal: [PayPal Adopts GraphQL: Gains Increased Developer Productivity](https://www.infoq.com/news/2021/10/paypal-graphql/)

* From Netflix: [Netflix Embraces GraphQL Microservices for Rapid Application Development](https://www.infoq.com/news/2021/03/netflix-graphql-microservices/)
* From Across Github, Airbnb & Shopify [GraphQL's Top Benefits Explained](https://dgraph.io/blog/post/advantages-of-graphql/)

## Optimization

- Using Dataloaders in [GraphQL Strawberry](https://strawberry.rocks/docs/guides/dataloaders#dataloaders)

### GraphQL is more ~~Beautiful~~ Restful than Rest

As a fairly new starter to TBN, I’m blessed with 1 big thing: The Bliss of Ignorance (inserts meme)
So in this presentation, there would be places where the answer would be – I didn’t know that.

However, I think I was hired at the right time, for this singular purpose – to bring this knowledge at this time.
A lot of decisions has been made from choice of Frontend – Javascript to choice of Backend – Python, to choice of Database - Postgres, and this does not change or impact on any of it.

REST is not a protocol or a standard, it is an architectural style. During the development phase, API developers can implement REST in a variety of ways.
Source: https://restfulapi.net/

Like the other architectural styles, REST also has its guiding principles and constraints. These principles must be satisfied if a service interface has to be referred to as RESTful.
A large number of people wrongly relate resource methods to HTTP methods (i.e., GET/PUT/POST/DELETE). Roy Fielding has never mentioned any recommendation around which method to use in which condition. All he emphasizes is that it should be a uniform interface.

The rise of GraphQL
[https://hasura.io/blog/the-rise-of-graphql-apis-on-data-warehouses](https://hasura.io/blog/the-rise-of-graphql-apis-on-data-warehouses)

It is essentially SQL on steroids for APIs
building an API that leads to the next level of data engineering, which I call Analytics API in this article. The API will empower all stakeholders to use one single source of accessing analytics data in a consistent and decoupled semantic way
https://www.ssp.sh/blog/analytics-api-with-graphql-the-next-level-of-data-engineering/

> We are a technology company that does Benchmarking – Sarah Atkinson Thu 18th, July 2024.

So in the end, what are you writing? You're not writing FastAPi, not Django, not GraphQL, but Python.
Absolute chaos!!!
~~No it is not that bad~~

- API Level and Definitions and Types are FastAPI/ GraphQL
- Business logic and models is Django
