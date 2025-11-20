import json
import os

# Define the robust function code
ROBUST_CODE = """def trajectory_reward(prompts, completions, answers=None, **kwargs):
    import jax.numpy as jnp
    # Attempt to get answers from kwargs if not provided positionally
    if answers is None:
        answers = kwargs.get('answers', [])

    rewards = []
    # Dynamically calculate group size to avoid shape mismatch errors
    batch_size = len(prompts)
    total_completions = len(completions)
    
    # Safety check
    if batch_size == 0:
        return jnp.array([])

    group_size = total_completions // batch_size
    
    for i, completion in enumerate(completions):
        batch_idx = i // group_size
        
        # Handle edge case where completions might not perfectly align
        if len(answers) == 0:
             target_answer = ""
        elif batch_idx >= len(answers):
            break
        else:
            target_answer = answers[batch_idx]

        score = 0.0
        
        # 1. Format Reward: Check for reasoning tags
        if "<reasoning>" in completion and "</reasoning>" in completion:
            score += 0.5
            
        # 2. Correctness Reward: Check if answer is correct
        if target_answer and target_answer in completion:
            score += 1.0
            
        rewards.append(score)
    
    # CRITICAL FIX: Reshape to (Batch, Group) for Tunix GRPO
    return jnp.array(rewards).reshape(batch_size, group_size)"""

def fix_notebook():
    input_filename = "winner-trajectory-reward-grpo-training-gemm (7).ipynb"
    output_filename = "winner_fixed.ipynb"
    
    print(f"Reading {input_filename}...")
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {input_filename}")
        return

    found = False
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            # Join source lines to check content
            source_text = "".join(cell['source'])
            if "def trajectory_reward" in source_text:
                print("Found trajectory_reward function. Replacing...")
                # Replace the entire cell content with the robust code
                cell['source'] = [ROBUST_CODE]
                found = True
                break
    
    if found:
        print(f"Writing fixed notebook to {output_filename}...")
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1)
        print("Success! Notebook fixed.")
    else:
        print("Error: Could not find the trajectory_reward function in the notebook.")

if __name__ == "__main__":
    fix_notebook()
