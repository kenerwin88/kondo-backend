from kondo_backend import repo_processor

if __name__ == "__main__":
    installations = repo_processor.get_installations.get_installations()
    print(installations)
    token = repo_processor.get_access_token.get_access_token("932356")
    print(token)
