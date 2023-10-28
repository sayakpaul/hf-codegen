# hf-codegen

A repository containing Python scripts for collating code content from the public repositories of `huggingface` on GitHub. 

Resultant dataset: https://huggingface.co/datasets/sayakpaul/hf-codegen-v2. 

**Update**: Sourab (@pacman100) and I published a blog post utilizing a part of this dataset to train a custom coding assistant. While I focused on data collection efforts, Sourab led the rest of the project, running numerous experiments. Check out our blog post here: P[ersonal Copilot: Train Your Own Coding Assistant](https://huggingface.co/blog/personal-copilot).

## To generate the dataset 

Make sure you have at least 50 GB of disk space.

1. Clone the repo and change to the `data` directory. 
2. Install the Python dependencies: `pip install -r requirements.`
3. Run `python parallel_clone_repos.py` to locally clone the public repositories situated under the `huggingface` GitHub org. You'd need to set up `GH_ACCESS_TOKEN` as the env variable (it can be your GitHub personal access token).
4. Log in to your HF account: `huggingface-cli login`.
5. Prepare the dataset, serialize in feather files, and upload them to the Hugging Face Hub: `python prepare_dataset.py`.
6. To finally have the dataset compatible with 🤗 Datasets (helps with downstream training), run `python push_to_hub.py`.

💡 Note that Step 6 was run on a separate machine with lots of RAM (240 GB). Steps 5 - 6 could have been clubbed together had we used a more capable machine from the get-go. 

The final dataset can be found here: [sayakpaul/hf-codegen-v2](https://hf.co/datasets/sayakpaul/hf-codegen-v2).

## Some lessons learned

Initially, we tried to also parallelize the reading and processing of code contents using `multiprocessing` but couldn't succeed in doing so. The memory was getting overhauled. 

So, we decided to process each repository file (in total we have 115 repositories) sequentially. [The utility](https://github.com/sayakpaul/hf-codegen/blob/c43da62dd95bd8ac1950bfc8e5c0cedbaf8d67a2/data/prepare_dataset.py#L75) returns a dictionary which we were appending to a `pandas` dataframe, which was initialized to be empty just containing columns. Our plan was to construct a final big `pandas` dataframe and serialize that.

This was failing to execute in full capacity as the memory was overhauling in this case too. 

So, we decided to serialize multiple dataframes in chunks to not overhaul the memory. Initially, we were serializing the dataframes in `.csv` format and the resultant CSV files were in GBs in terms of size. So, we finally decided to use the Feather format for serialization which resulted in much lighter files (from a GB to 300 MB, for example). 
