Make sure you have at least 50 GB of disk space.

1. Install the Python dependencies: `pip install -r requirements.`
2. Run `python parallel_clone_repos.py` to locally clone the public repositories situated under the `huggingface` GitHub org. You'd need to set up `GH_ACCESS_TOKEN` as the env variable (it can be your GitHub personal access token).
3. Log in to your HF account: `huggingface-cli login`.
4. Prepare the dataset and push it to the Hugging Face Hub: `python prepare_dataset.py`.