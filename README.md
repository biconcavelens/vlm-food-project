# Food Instruction Generator using CLIP

A system that generates cooking instructions by matching food images and vague descriptions using CLIP (Contrastive Language-Image Pre-Training) model.

## Overview

This project uses OpenAI's CLIP model to:
1. Process food images and vague text descriptions
2. Match them with known recipes
3. Generate appropriate cooking instructions

## Features

- Image-text similarity matching using CLIP
- Support for vague/informal food descriptions
- 10 different food categories with multiple examples
- Evaluation metrics (ROUGE, BLEU scores)
- Both detailed and concise cooking instructions

## Project Structure

```
vlm food project/
├── images/
│   ├── burger/
│   ├── curry/
│   ├── pasta/
│   └── ... (other food categories)
├── main.py              # Core instruction generation logic
├── food_dataset.py      # Dataset management
├── add_samples.py       # Dataset population
└── evaluate_accuracy.py # Accuracy evaluation
```

## Setup

1. Install dependencies:
```bash
pip install transformers torch Pillow rouge-score nltk
```

2. Prepare the dataset:
```bash
python add_samples.py
```

3. Run the program:
```bash
python main.py
```

## How It Works

1. **Image Processing**:
   - Uses CLIP's vision encoder to extract image features
   - Processes both test images and dataset samples

2. **Text Processing**:
   - Encodes vague food descriptions using CLIP's text encoder
   - Compares semantic similarity of descriptions

3. **Matching**:
   - Combines image and text similarity scores
   - Finds best matching recipe from dataset
   - Returns appropriate cooking instructions

## Example Usage

```python
# Input a test image and vague description
image_path = "images/test/test_pasta1.png"
vague_title = "cheesy noodly thing"

# Get cooking instructions
result = generator.generate_instructions(image_path, vague_title)
```

## Evaluation

Run accuracy evaluation:
```bash
python evaluate_accuracy.py
```

The evaluation:
- Tests multiple images per category
- Calculates ROUGE and BLEU scores
- Reports matching accuracy
- Provides detailed similarity metrics

## Dataset

Currently includes 10 food categories:
- Burger
- Chole Bature
- Curry
- Omelette
- Pasta
- Pizza
- Salad
- Soup
- Sushi
- Tacos

Each category contains:
- 10 training images
- Formal recipe name
- Vague/informal title
- Detailed instructions
- Concise 2-3 step summary
