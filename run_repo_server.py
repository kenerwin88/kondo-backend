from kondo_backend import repo_processor

if __name__ == "__main__":
    repo_processor.process_repositories()  # Process every repository and store data in redis
