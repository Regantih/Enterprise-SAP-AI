import json

def fix_matplotlib_version_v5():
    input_filename = "winner_fixed_v2.ipynb" # Start from the clean V2
    output_filename = "winner_fixed_v5.ipynb"
    
    print(f"Reading {input_filename}...")
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {input_filename}")
        return

    # Create the fix cell - Upgrade Matplotlib instead of downgrading NumPy
    fix_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# CRITICAL FIX: Upgrade Matplotlib to support NumPy 2.0\n",
            "# This avoids downgrading NumPy which breaks JAX/ml_dtypes\n",
            "!pip install \"matplotlib>=3.9.0\" --force-reinstall\n",
            "import matplotlib\n",
            "print(f\"Matplotlib Version: {matplotlib.__version__}\")"
        ]
    }
    
    # Insert at the very beginning
    notebook['cells'].insert(0, fix_cell)
    
    print(f"Writing fixed notebook to {output_filename}...")
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)
    print("✅ Success! Added Matplotlib upgrade cell.")

if __name__ == "__main__":
    fix_matplotlib_version_v5()
