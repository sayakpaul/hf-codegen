## To generate the dataset 

Make sure you have at least 50 GB of disk space.

1. Install the Python dependencies: `pip install -r requirements.`
2. Run `python parallel_clone_repos.py` to locally clone the public repositories situated under the `huggingface` GitHub org. You'd need to set up `GH_ACCESS_TOKEN` as the env variable (it can be your GitHub personal access token).
3. Log in to your HF account: `huggingface-cli login`.
4. Prepare the dataset and push it to the Hugging Face Hub: `python prepare_dataset.py`.

## Some lessons learned

Initially, we tried to also parallelize the reading and processing of code contents using `multiprocessing` but couldn't succeed in doing so. The memory was getting overhauled. 

So, we decided to process each repository file (in total we have 115 repositories) sequentially. The utility returns a dictionary which we were appending to a `pandas` dataframe, which was initialized to be empty just containing columns. Our plan was to construct a final big `pandas` dataframe and serialize that.

This was failing to execute in full capacity as the memory was overhauling in this case too. 

So, we decided to serialize multiple dataframes in chunks to not overhaul the memory. Initially, we were serializing the dataframes in `.csv` format and the resultant CSV files were in GBs in terms of size. So, we finally decided to use the Feather format for serialization which resulted in much lighter files (from a GB to 300 MB, for example). 

