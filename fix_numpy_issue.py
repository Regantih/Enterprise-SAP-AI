import json

def fix_numpy_version():
    input_filename = "winner_fixed_v2.ipynb"
    output_filename = "winner_fixed_v3.ipynb"
    
    print(f"Reading {input_filename}...")
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {input_filename}")
        return

    # Create the fix cell
    fix_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# CRITICAL FIX: Downgrade NumPy to <2.0 to fix matplotlib compatibility issues\n",
            "!pip install \"numpy<2.0\" --force-reinstall\n",
            "import os\n",
            "os.kill(os.getpid(), 9) # Restart kernel to apply changes"
        ]
    }
    
    # Insert at the very beginning
    notebook['cells'].insert(0, fix_cell)
    
    print(f"Writing fixed notebook to {output_filename}...")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)
    print("✅ Success! Added NumPy downgrade cell.")

if __name__ == "__main__":
    fix_numpy_version()
