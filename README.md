# **Stable diffusion discord bot**
Users can generate images simply with a command.


#### Requirements:
- A strong GPU, preferrably with 8GB VRAM
- 16GB RAM or more
- ComfyUI: [ComfyUI](https://github.com/comfyanonymous/ComfyUI)

# **Quick start**
- Run ComfyUI (run_cpu or run_nvidia_gpu if you have an nvidia gpu)
- Replace the placeholder "YOUR MODEL NAME" in workflow_api.json, on line 31.
- Once comfyUI is running, replace the server_address in StableDiffusion.py with your current url (Default is 127.0.0.1:8188)
- Run Main.py
- Use the command "/gen"
