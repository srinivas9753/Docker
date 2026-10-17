import os
name = os.getenv("APP_NAME", "Docker learner")
print(f"Hello, {name}!")
print("Python is running inside a container.")