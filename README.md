# **Stable cascade discord bot**
This discord bot interfaces with the ComfyUI API.

Stable cascade is a remarkable text-to-image model that can work at a very small latent space. In other words, stable cascade is able to compress images from 1024x1024 to 24x24 pixels without losing details.
This allows for a faster generation time, while achieving a 16x cost reduction over Stable Diffusion 1.5.



# **Requirements:**
- A strong GPU, preferrably with 8GB VRAM
- 16GB RAM or more
- ComfyUI: [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
  
### Stable cascade models installation guide (Install ComfyUI first before proceeding):
Download and install the following models into \ComfyUI\models\unet
- [stage_b](https://huggingface.co/stabilityai/stable-cascade/blob/main/stage_b_bf16.safetensors)
- [stage_c](https://huggingface.co/stabilityai/stable-cascade/blob/main/stage_c_bf16.safetensors)
  
Download and install the following model into \ComfyUI\models\vae
- [stage_a](https://huggingface.co/stabilityai/stable-cascade/blob/main/stage_a.safetensors)
  
Download and install the following model into \ComfyUI\models\clip
- [text_encoder](https://huggingface.co/stabilityai/stable-cascade/blob/main/text_encoder/model.safetensors)
# **Quick start**
- Run ComfyUI (run_cpu or run_nvidia_gpu if you have an nvidia gpu)
- Once comfyUI is running, replace the ```server_address``` in StableDiffusion.py with your current url ```(Default is 127.0.0.1:8188)```
- Ensure that your discord bot is setup.
- Run Main.py
- Use the command ```/gen```
