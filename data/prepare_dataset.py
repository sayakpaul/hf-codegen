import os
import pandas as pd
from nbformat import reads, NO_CONVERT
import pygit2
from multiprocessing import Pool
from datasets import Dataset

MIRROR_DIRECTORY = "hf_public_repos"
DATASET_ID = "hf-codegen"


def filter_code_cell(cell):
    """Filters a code cell w.r.t shell commands, etc."""
    only_shell = cell["source"].startswith("!")
    only_magic = "%%capture" in cell["source"]
    if only_shell or only_magic:
        return False
    else:
        return True


def process_file(file_path):
    repository_path, relative_path = file_path
    repository = pygit2.Repository(repository_path)
    commit = repository.head.target

    try:
        blob = repository[commit.tree_id / relative_path]
        content = blob.data.decode("utf-8")
        if relative_path.endswith("ipynb"):
            code_cell_str = ""
            notebook = reads(content, NO_CONVERT)

            code_cells = [
                c
                for c in notebook["cells"]
                if c["cell_type"] == "code"
                if filter_code_cell(c)
            ]

            for cell in code_cells:
                code_cell_str += cell["source"]
            content = code_cell_str
    
    except (KeyError, pygit2.GitError):
        # Handle cases where the file is not found or cannot be read
        content = ""

    return {
        "directory_name": os.path.dirname(file_path),
        "filepath": file_path,
        "content": content
    }


def read_repository_files(directory):
    file_paths = []

    # Recursively find all files within the directory
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append((directory, file_path))

    # Process files using multiprocessing
    print(f"Total file paths: {len(file_paths)}.")
    with Pool() as pool:
        results = pool.map(process_file, file_paths)

    return pd.DataFrame(results)


if __name__ == "__main__":
    df = read_repository_files(MIRROR_DIRECTORY)
    print("DataFrame created, creating dataset...")
    dataset = Dataset.from_pandas(df)
    dataset.push_to_hub(DATASET_ID, private=True)
