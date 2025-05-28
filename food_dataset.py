import json
from pathlib import Path

class FoodDataset:
    def __init__(self):
        self.samples = []
        self.dataset_file = "food_samples.json"

    def add_sample(self, actual_name, image_paths, vague_title, full_instructions, concise_steps):
        """Add a sample to the dataset with single or multiple image paths"""
        sample = {
            "actual_name": actual_name,
            "image_paths": image_paths if isinstance(image_paths, list) else [image_paths],
            "vague_title": vague_title,
            "full_instructions": full_instructions,
            "concise_steps": concise_steps
        }
        self.samples.append(sample)

    def save_dataset(self):
        with open(self.dataset_file, 'w') as f:
            json.dump(self.samples, f, indent=4)

    def load_dataset(self):
        if Path(self.dataset_file).exists():
            with open(self.dataset_file, 'r') as f:
                self.samples = json.load(f)