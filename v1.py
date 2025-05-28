from food_dataset import FoodDataset
from transformers import AutoProcessor, CLIPVisionModel
from PIL import Image
import torch
from pathlib import Path

class FoodInstructionGenerator:
    def __init__(self):
        # Initialize vision model and processor
        self.vision_model = CLIPVisionModel.from_pretrained("openai/clip-vit-base-patch32",local_files_only=True)
        self.processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32",local_files_only=True)
        self.dataset = FoodDataset()
        self.dataset.load_dataset()

    def process_image(self, image_path):
        """Process a single image and return its features"""
        image = Image.open(image_path)
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.vision_model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)

    '''def generate_instructions(self, image_path, vague_title):
        """Generate cooking instructions for a new image-title pair"""
        # Process new image
        image_features = self.process_image(image_path)
        
        # Find most similar example from dataset
        best_match = None
        best_similarity = -1

        for sample in self.dataset.samples:
            # Process each sample image and compare
            for sample_image in sample["image_paths"]:
                sample_features = self.process_image(sample_image)
                similarity = torch.cosine_similarity(image_features, sample_features)
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = sample
                    matched_similarity = similarity.item()  # Convert tensor to number
            
        if best_match:
            return{
                "title": best_match["vague_title"],
                "steps": best_match["conscise_steps"],
                "best_match": best_match,
                "similarity": matched_similarity
            }
        else:
            print("No suitable match found in dataset.")
            return None'''
    def generate_instructions(self, image_path, vague_title):
        """Generate cooking instructions for a new image-title pair"""
        # Process new image
        image_features = self.process_image(image_path)
    
        # Find most similar example from dataset
        best_match = None
        best_similarity = -1

        for sample in self.dataset.samples:
            # Process each sample image and compare
            for sample_image in sample["image_paths"]:
                sample_features = self.process_image(sample_image)
                similarity = torch.cosine_similarity(image_features, sample_features)
            
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = sample
                    matched_similarity = similarity.item()  # Convert tensor to number
        
        if best_match:
            return {
                "title": best_match["actual_name"],
                "steps": best_match["concise_steps"],  # Fixed typo here
                "best_match": best_match,
                "similarity": matched_similarity
            }
        else:
            print("No suitable match found in dataset.")
            return None

def main():
    print("Starting FoodInstructionGenerator...")
    generator = FoodInstructionGenerator()
    
    # Example usage
    test_image = "images/test_tacos.png"
    title = input("Enter a vague title for the dish (e.g., 'cheesy noodly thing'): ").strip()
    
    print(f"\nProcessing:")
    print(f"- Image: {test_image}")
    print(f"- Title: {title}")
    
    # Check if dataset loaded properly
    print(f"\nDataset status:")
    print(f"- Number of samples: {len(generator.dataset.samples)}")
    if len(generator.dataset.samples) == 0:
        print("WARNING: Dataset is empty! Run add_samples.py first.")
        return
    
    # Generate and display instructions
    print("\nGenerating instructions...")
    result = generator.generate_instructions(test_image, title)
    
    print("\nResults:")
    if result:
        print(f"Matched recipe: {result['title']}")
        print(f"Similarity score: {result['similarity']:.2f}")
        print("\nGenerated instructions:")
        for i, step in enumerate(result['steps'], 1):
            print(f"{i}. {step}")
    else:
        print("No instructions generated. Possible issues:")
        print("- Check if test_image exists in images folder")
        print("- Verify food_samples.json contains valid data")

if __name__ == "__main__":
    main()