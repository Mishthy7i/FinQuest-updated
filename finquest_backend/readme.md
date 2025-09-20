# FinQuest Backend

A simple backend using FastAPI and MySQL

1. create venv
   python -m venv myenv
2. use venv
   ./myenv/Scripts/activate   
3. install fastapi
   pip install -r requirements.txt
4. start fastapi
    uvicorn main:app --port 7001 --reload

we used DECIMAL(10, 2) datatype to store salary.

we can view api docs and test them on fastapi docs
- http://localhost:8000/docs

routes-
post on /auth/signup to register.
post on /auth/login to login and get jwt token, now for any request to server, send that token in authorization headers.
post on /auth/testjwt to test if jwt works, when testing with swagger, set token by clicking on lock icon.

resources
- https://fastapi.tiangolo.com/tutorial/first-steps/
- https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- https://testdriven.io/blog/fastapi-jwt-auth/
 
 
 ## Backend is hosted using render 
 ### URL="https://finavengers-render-1.onrender.com"
 ### Swagger="https://finavengers-render-1.onrender.com/docs"
