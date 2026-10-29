import os
import torch
from diffusers import StableDiffusionPipeline
from diffusers import ZImagePipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image, ImageTk

from google import genai
from google.genai import types
from PIL import Image

# Ideas
# - Chatbot with different sessions
# - suffix preset
# - Gemini - Generation Image Nanobanana

# Fluffy Cat with extremely detailed realistic fur, individual hair strands visible, soft warm lighting, natural outdoor environment, sitting in grass with subtle wind movement, photorealistic rendering, cinematic lighting, volumetric light, global illumination, shallow depth of field, bokeh background, 85mm lens, ultra realistic textures, sharp focus, 8k, DSLR photography style

# ----------------------------------- UI VERSION (DREAMLIKE) -----------------------------------
os.environ["HF_TOKEN"] = "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"

# MODEL 1:
model_id = "dreamlike-art/dreamlike-photoreal-2.0"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe = pipe.to("cuda")
pipe.enable_attention_slicing()

def generate_image(prompt, output_filename, width = 768, height = 768, steps = 50):

    folder_name = "generated_images"
    os.makedirs(folder_name, exist_ok=True)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    filename = output_filename + ".png"
    file_path = os.path.join(folder_name, filename)

    # Output
    print("Generating...")

    # ONLY FOR FIRST MODEL
    neg_prompt = (
        "blurry, out of focus, low quality, soft edges, distorted, "
        "deformed, extra limbs, bad anatomy, watermark, text, grainy"
    )

    prompt_enhancement = (
        "photorealistic rendering, cinematic lighting, volumetric light, "
        "global illumination, shallow depth of field, bokeh background, 85mm lens, "
        "ultra realistic textures, sharp focus, 8k, DSLR photography style"
    )

    with torch.inference_mode():
        with torch.autocast("cuda", dtype = torch.float16):
            image = pipe(
                prompt + prompt_enhancement,
                num_inference_steps= steps, # how many steps to refine image,
                guidance_scale = 8.5,
                width = width,
                height = height,

                negative_prompt = neg_prompt
            ).images[0]


    # Save the result
    image.save(file_path)
    print(f"Image saved as {folder_name} as {filename}")

    return file_path
