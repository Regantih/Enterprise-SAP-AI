import json
import os

# Updated reward functions with proper shape handling
UPDATED_REWARDS = {
    "match_format_exactly": """def match_format_exactly(prompts, completions, **kwargs):
  import jax.numpy as jnp
  rewards = [
      0 if match_format.search(response) is None else 3.0
      for response in completions
  ]
  # Ensure 1D array
  return jnp.array(rewards).flatten()""",
    
    "match_format_approximately": """def match_format_approximately(prompts, completions, **kwargs):
  import jax.numpy as jnp
  scores = []

  for completion in completions:
    score = 0
    response = completion
    score += 0.5 if response.count(reasoning_start) == 1 else -0.5
    score += 0.5 if response.count(reasoning_end) == 1 else -0.5
    score += 0.5 if response.count(solution_start) == 1 else -0.5
    score += 0.5 if response.count(solution_end) == 1 else -0.5
    scores.append(score)
  # Ensure 1D array
  return jnp.array(scores).flatten()""",
    
    "check_answer": """def check_answer(prompts, completions, answer, **kwargs):
  import jax.numpy as jnp
  responses = completions

  extracted_responses = [
      guess.group(1) if (guess := match_format.search(r)) is not None else None
      for r in responses
  ]

  scores = []
  assert len(extracted_responses) == len(
      answer
  ), f"{extracted_responses} and {answer} have mismatching length"
  for guess, true_answer in zip(extracted_responses, answer):
    score = 0
    if guess is None:
      scores.append(0)
      continue
    if guess == true_answer:
      score += 3.0
    elif guess.strip() == true_answer.strip():
      score += 1.5
    else:
      try:
        ratio = float(guess) / float(true_answer)
        if ratio >= 0.9 and ratio <= 1.1:
          score += 0.5
        elif ratio >= 0.8 and ratio <= 1.2:
          score += 0.25
        else:
          score -= 1.0
      except:
        score -= 0.5
    scores.append(score)
  # Ensure 1D array
  return jnp.array(scores).flatten()""",
    
    "check_numbers": """def check_numbers(prompts, completions, answer, **kwargs):
  import jax.numpy as jnp
  question = kwargs["question"]
  responses = completions

  extracted_responses = [
      guess.group(1) if (guess := match_numbers.search(r)) is not None else None
      for r in responses
  ]

  scores = []
  print("START ============================")
  print(f"Question: {question[0]}")
  print(f"Answer: {answer[0]}")
  print(f"Response: {responses[0]}")
  print(f"Extracted: {extracted_responses[0]}")
  print("END ==============================")
  for guess, true_answer in zip(extracted_responses, answer):
    if guess is None:
      scores.append(0)
      continue
    try:
      true_answer = float(true_answer.strip())
      guess = float(guess.strip())
      scores.append(1.5 if guess == true_answer else 0.0)
    except:
      scores.append(0)
      continue
  # Ensure 1D array
  return jnp.array(scores).flatten()""",
    
    "trajectory_reward": """def trajectory_reward(prompts, completions, answers=None, **kwargs):
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
}

def fix_all_reward_functions():
    input_filename = "winner-trajectory-reward-grpo-training-gemm (7).ipynb"
    output_filename = "winner_fixed_v2.ipynb"
    
    print(f"Reading {input_filename}...")
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {input_filename}")
        return

    functions_found = {key: False for key in UPDATED_REWARDS.keys()}
    
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source_text = "".join(cell['source'])
            
            # Check each reward function
            for func_name, new_code in UPDATED_REWARDS.items():
                if f"def {func_name}" in source_text and not functions_found[func_name]:
                    print(f"Found {func_name}. Replacing...")
                    cell['source'] = [new_code]
                    functions_found[func_name] = True
                    break
    
    # Report findings
    for func_name, found in functions_found.items():
        if found:
            print(f"✅ Updated {func_name}")
        else:
            print(f"⚠️  Could not find {func_name}")
    
    if any(functions_found.values()):
        print(f"\nWriting fixed notebook to {output_filename}...")
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1)
        print("✅ Success! All reward functions fixed.")
    else:
        print("❌ Error: Could not find any reward functions in the notebook.")

if __name__ == "__main__":
    fix_all_reward_functions()
