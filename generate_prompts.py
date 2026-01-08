import json

with open('/home/neuralspark/.gemini/antigravity/brain/218b7391-bee4-437e-8ba3-d3be0bc555a0/illustration_assets.json', 'r') as f:
    data = json.load(f)

global_style = data.get('global_style_prompt', '')
global_neg = data.get('global_negative_prompt', '')

for img in data['images']:
    aspect = img.get('aspect_ratio', '')
    aspect_str = f"{aspect.capitalize()} format" if aspect else ""
    
    # Constructing the full prompt
    # User rule: global_style_prompt + images[n].base_prompt + images[n].negative_prompt
    # Assuming images[n].negative_prompt refers to global_negative_prompt as per JSON structure absent local negs.
    
    base = img.get('base_prompt', '')
    
    # We'll use the "Negative prompt:" syntax if the model supports it, but standard might be just adding it.
    # However, standard practice for these tools if they don't support neg prompt arg is just text.
    # But user asked to concatenate.
    
    full_prompt = f"{global_style} {base} {global_neg}"
    
    # Prepending aspect ratio instruction to help the model
    final_prompt = f"{aspect_str}. {full_prompt}"
    
    # Outputting in a format I can easily use or read
    print(f"ID: {img['id']}")
    print(f"Name: {img['id'].lower()}_{img['title'].lower().replace(' ', '_').replace('-', '_').replace('/', '_')}")
    print(f"Prompt: {final_prompt}")
    print("-" * 20)
