# FastAPI application setup
from fastapi import FastAPI
from routes import router  # Importing the router from routes.py

app = FastAPI()  # Creating a new FastAPI application instance
app.include_router(router)  # Including the router in the application

# Running the application with Uvicorn if this file is executed as the main program
if __name__ == "__main__":
    import uvicorn  # Importing Uvicorn programmatically
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Running the app on localhost port 8000