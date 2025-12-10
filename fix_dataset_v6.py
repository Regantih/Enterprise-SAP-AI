import json

def fix_dataset_attachment_v6():
    input_filename = "winner_fixed_v5.ipynb" # Start from V5 (has matplotlib fix)
    output_filename = "winner_fixed_v6.ipynb"
    
    print(f"Reading {input_filename}...")
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {input_filename}")
        return

    # Add metadata for Kaggle to pre-attach the dataset
    if 'metadata' not in notebook:
        notebook['metadata'] = {}
    
    if 'kaggle' not in notebook['metadata']:
        notebook['metadata']['kaggle'] = {}
    
    # Add the dataset to data_sources
    notebook['metadata']['kaggle']['data_sources'] = [
        {
            "datasetId": "thedevastator/grade-school-math-8k-q-a",
            "sourceId": "5969154",
            "sourceType": "datasetVersion"
        }
    ]
    
    print(f"Writing fixed notebook to {output_filename}...")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)
    print("✅ Success! Added dataset to metadata.")

if __name__ == "__main__":
   fix_dataset_attachment_v6()
