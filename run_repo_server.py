from kondo_backend import repo_processor

if __name__ == "__main__":
    repo_processor.process_repositories()
    # installations = repo_processor.get_installations()
    # print(installations)
    # token = repo_processor.get_access_token("932356")
    # print(token)
    # print(repo_processor.get_installation_repositories(token))
