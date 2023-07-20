from huggingface_hub import snapshot_download
from datasets import Dataset
from tqdm import tqdm
import pandas as pd
import glob

REPO_ID = "sayakpaul/hf-codegen"
FEATHER_FORMAT = "*.ftr"

if __name__ == "__main__":
    folder_path = snapshot_download(
        repo_id=REPO_ID, allow_patterns=f"*.{FEATHER_FORMAT}", repo_type="dataset"
    )
    feather_files = glob.glob(f"{folder_path}/raw_csvs/*.{FEATHER_FORMAT}")
    print(folder_path, len(feather_files))

    all_dfs = []

    for feather_file in tqdm(feather_files):
        df = pd.read_feather(feather_file)
        all_dfs.append(df)

    final_df = pd.concat(all_dfs)
    print(f"Final DF prepared containing {len(final_df)} rows.")

    dataset = Dataset.from_pandas(final_df)
    dataset.push_to_hub("hf-codegen-v2")
