import torch
from PIL import Image
import requests
from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration, BitsAndBytesConfig
import time
from io import BytesIO
import gc
import os

# Set environment variables for better memory management
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:32'

def clear_gpu_memory():
    """Clear GPU memory cache"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()

def test_llava_model():
    """
    Test the LLaVA-v1.6-mistral-7b-hf model with image and text input
    Optimized for memory efficiency
    """
    
    # Clear initial memory
    clear_gpu_memory()
    
    # Check if CUDA is available
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
        print("Running on GPU")
        # Limit GPU memory usage to 80% of available
        torch.cuda.set_per_process_memory_fraction(0.8)
    else:
        device = torch.device("cpu")
        print("Running on CPU")
    
    # Configure quantization for memory efficiency
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )
    
    # Load the model and processor with memory optimizations
    print("Loading model and processor...")
    try:
        processor = LlavaNextProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
        model = LlavaNextForConditionalGeneration.from_pretrained(
            "llava-hf/llava-v1.6-mistral-7b-hf", 
            torch_dtype=torch.float16, 
            low_cpu_mem_usage=True,
            quantization_config=quantization_config if torch.cuda.is_available() else None,
            device_map="auto"
        )
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Trying without quantization...")
        model = LlavaNextForConditionalGeneration.from_pretrained(
            "llava-hf/llava-v1.6-mistral-7b-hf", 
            torch_dtype=torch.float16, 
            low_cpu_mem_usage=True,
            device_map="auto"
        )
    
    # Test with different images and prompts
    test_cases = [
        {
            "image_url": "https://github.com/haotian-liu/LLaVA/blob/1a91fc274d7c35a9b50b3cb29c4247ae5837ce39/images/llava_v1_5_radar.jpg?raw=true",
            "prompt": "What is shown in this image?"
        },
        {
            "image_url": "https://h2o-release.s3.amazonaws.com/h2ogpt/bigben.jpg",
            "prompt": "Describe the architecture and location of this landmark."
        },
        {
            "image_url": "https://github.com/haotian-liu/LLaVA/blob/1a91fc274d7c35a9b50b3cb29c4247ae5837ce39/images/llava_v1_5_radar.jpg?raw=true",
            "prompt": "Extract any text visible in this image."
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"Test Case {i}")
        print(f"{'='*50}")
        
        try:
            # Clear memory before each test case
            clear_gpu_memory()
            
            # Load image from URL with timeout
            print(f"Loading image from: {test_case['image_url']}")
            response = requests.get(test_case['image_url'], stream=True, timeout=30)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content)).convert("RGB")
            
            # Resize image if too large to save memory
            max_size = 1024
            if max(image.size) > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                print(f"Image resized to: {image.size}")
            else:
                print(f"Image loaded successfully. Size: {image.size}")
            
            # Prepare conversation
            conversation = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": test_case['prompt']},
                        {"type": "image"},
                    ],
                },
            ]
            
            # Apply chat template
            prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
            
            # Prepare inputs
            inputs = processor(images=image, text=prompt, return_tensors="pt")
            
            # Move inputs to device
            if torch.cuda.is_available():
                inputs = {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}
            
            # Generate response with memory-efficient settings
            print(f"Prompt: {test_case['prompt']}")
            print("Generating response...")
            
            start_time = time.time()
            with torch.no_grad():
                output = model.generate(
                    **inputs, 
                    max_new_tokens=150,  # Reduced from 200
                    pad_token_id=processor.tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    use_cache=False,  # Disable KV cache to save memory
                    num_beams=1  # Use greedy search instead of beam search
                )
            generation_time = time.time() - start_time
            
            # Decode and print response
            response = processor.decode(output[0], skip_special_tokens=True)
            
            # Extract only the generated part (remove the input prompt)
            if "[/INST]" in response:
                generated_text = response.split("[/INST]")[-1].strip()
            else:
                # Fallback if the format is different
                generated_text = response[len(prompt):].strip()
            
            print(f"Response: {generated_text}")
            print(f"Generation time: {generation_time:.2f} seconds")
            
            # Clear memory after generation
            del output, inputs
            clear_gpu_memory()
            
        except torch.cuda.OutOfMemoryError:
            print(f"CUDA out of memory in test case {i}. Clearing cache and continuing...")
            clear_gpu_memory()
            continue
        except Exception as e:
            print(f"Error in test case {i}: {str(e)}")
            clear_gpu_memory()
            continue
    
    print(f"\n{'='*50}")
    print("Testing completed!")

def test_with_local_image(image_path, prompt):
    """
    Test the model with a local image file - memory optimized version
    """
    print("Testing with local image...")
    
    # Clear memory
    clear_gpu_memory()
    
    # Setup device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        torch.cuda.set_per_process_memory_fraction(0.8)
    
    # Configure quantization
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    ) if torch.cuda.is_available() else None
    
    # Load model and processor
    processor = LlavaNextProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
    model = LlavaNextForConditionalGeneration.from_pretrained(
        "llava-hf/llava-v1.6-mistral-7b-hf", 
        torch_dtype=torch.float16, 
        low_cpu_mem_usage=True,
        quantization_config=quantization_config,
        device_map="auto"
    )
    
    try:
        # Load local image
        image = Image.open(image_path).convert("RGB")
        
        # Resize if necessary
        max_size = 1024
        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Prepare conversation
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image"},
                ],
            },
        ]
        
        # Process and generate
        formatted_prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
        inputs = processor(images=image, text=formatted_prompt, return_tensors="pt")
        
        if torch.cuda.is_available():
            inputs = {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}
        
        with torch.no_grad():
            output = model.generate(
                **inputs, 
                max_new_tokens=150,
                use_cache=False,
                num_beams=1
            )
        
        response = processor.decode(output[0], skip_special_tokens=True)
        if "[/INST]" in response:
            generated_text = response.split("[/INST]")[-1].strip()
        else:
            generated_text = response[len(formatted_prompt):].strip()
        
        print(f"Local image analysis: {generated_text}")
        
    except Exception as e:
        print(f"Error with local image: {str(e)}")
    finally:
        clear_gpu_memory()

if __name__ == "__main__":
    # Run the main test
    #test_llava_model()
    
    # Uncomment the line below to test with a local image
    test_with_local_image("image.jpg", "What do you see in this image?")
