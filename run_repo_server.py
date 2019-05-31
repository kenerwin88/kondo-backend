from kondo_backend import repo_processor

if __name__ == "__main__":
    installations = repo_processor.get_installations.get_installations()
    print(installations)
