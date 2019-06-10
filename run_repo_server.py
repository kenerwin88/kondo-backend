from kondo_backend import room_engine
from kondo_backend import repo_processor

if __name__ == "__main__":
    room_engine.initialize_rooms()  # Load all the rooms into memory
    repo_processor.process_repositories()  # Process every repository and store data in redis
