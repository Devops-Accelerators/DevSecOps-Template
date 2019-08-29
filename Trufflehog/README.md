# Trufflehog
Searches through git repositories for secrets, digging deep into commit history and branches. This is effective at finding secrets accidentally committed. This guide runs a trufflehog container on a machine which will search if any secrets are commited.

    ```
    NOTE: Need to have docker installed on the host from where you'll run the trufflehog container.
    ```

# Getting Started

-  Add the following lines in your Jenkins stage.

    ```
    docker run gesellix/trufflehog --json --regex <your_git_repo_url>
    ```
