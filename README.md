# FastAPI

[![LOGO](fcc.png)](https://www.freecodecamp.org/)
<img src="Fastapi.png" alt="drawing" width="200"/>
<img src="py.jpg" alt="drawing" width="50"/>

Link for more information about [FastAPI](https://fastapi.tiangolo.com/) or [python](https://www.python.org/).
- Python API Development - Comprehensive Course for Beginners

A restful crud api with python using fastapi framework.
[SWAGGER](http://127.0.0.1:8000/docs#/) docs.

### About Swagger

- Swagger is a powerful yet easy-to-use suite of API developer tools for teams and individuals, enabling development across the entire API lifecycle, from design and documentation, to test and deployment.

- Swagger consists of a mix of open source, free and commercially available tools that allow anyone, from technical engineers to street smart product managers to build amazing APIs that everyone loves.

- Swagger is built by SmartBear Software, the leader in software quality tools for teams. SmartBear is behind some of the biggest names in the software space, including Swagger, SoapUI and QAComplete.


## The History Behind Swagger

- Swagger started out as a simple, open source specification for designing RESTful APIs in 2010. Open source tooling like the Swagger UI, Swagger Editor and the Swagger Codegen were also developed to better implement and visualize APIs defined in the specification. The Swagger project, consisting of the specification and the open source tools, became immensely popular, creating a massive ecosystem of community driven tools.

- In 2015, the Swagger project was acquired by SmartBear Software. The Swagger Specification was donated to the Linux foundation and renamed the OpenAPI

- Specification to formally standardize the way REST APIs are described. The OpenAPI Initiative was created to guide the development of the OAS in an open and transparent manner.

- Swagger has since become the most popular suite of tools to fully leverage the power of the OAS across the API lifecycle.


### CRUD
- GET     endpoint ('/')
- POST    endpoint ("/posts")
- DELETE  endpoint ('/posts/{id}')
- PUT     endpoint ('/posts/{id}')


### database

- PostgresSQL

Psycopg: Drive for postgres database

```sql
-- Run this command with the following options:

docker run --name postgres-py -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres
```
- docker run: Run the Docker
- --name postgres-py: Name of the container
- -p 5432:5432: This is the port that will be used to connect to the postgres server.
- -e POSTGRES_PASSWORD=postgres: Create a password for the postgres server.
- -d postgres: The postgres server will connect.


### ORM sqlachemy

- The Python SQL Toolkit and Object Relational Mapper
  
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.


### Passlib and Bcrypt

- Hashing the password using passlib to cryptographically 


### JSON Web Tokens

- Or JWT. What is JSON Web Token?
  
JSON Web Token (JWT) is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA.

Although JWTs can be encrypted to also provide secrecy between parties, we will focus on signed tokens. Signed tokens can verify the integrity of the claims contained within it, while encrypted tokens hide those claims from other parties. When tokens are signed using public/private key pairs, the signature also certifies that only the party holding the private key is the one that signed it.

### Bcrypt

- Acceptable password hashing for your software and your servers (but you should really use argon2id or scrypt)

```bash
$ pip install bcrypt
```