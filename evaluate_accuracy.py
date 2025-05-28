from food_dataset import FoodDataset
from transformers import AutoProcessor, CLIPVisionModel
from PIL import Image
import torch
from pathlib import Path
import glob
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu
import nltk
from main import FoodInstructionGenerator

def evaluate_all_test_images():
    """Evaluate accuracy of instruction generation on all test images."""
    print("Starting accuracy evaluation...")
    generator = FoodInstructionGenerator()
    
    # Initialize metrics
    rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    nltk.download('punkt', quiet=True)
    
    total_tests = 0
    correct_matches = 0
    rouge_scores = []
    bleu_scores = []
    
    # Get all test images
    test_images = glob.glob("images/test/test_*[12].png")

    # Dictionary mapping food items to their vague titles
    vague_titles = {
        "pasta": "indian food",
        "curry": "spicy sauce with meat and veggies",
        "pizza": "italian pizza",
        "burger": "stacked meaty sandwich thing",
        "tacos": "mexican folded crunchy flavor holders",
        "soup": "warm liquid comfort food",
        "salad": "fresh crunchy vegetable mix",
        "sushi": "rolled rice and fish",
        "omelette": "fluffy egg pancake with fillings",
        "chole_bature": "spicy chickpeas with fluffy balloons"
    }

    for test_image in sorted(test_images):
        # Extract food item name from filename
        food_item = test_image.split('test_')[1].split('1.png')[0].split('2.png')[0]
        
        # Get corresponding vague title
        vague_title = vague_titles.get(food_item, "")

        # Generate instructions
        result = generator.generate_instructions(test_image, vague_title)
        
        if result:
            # Find ground truth from dataset
            ground_truth = next((sample for sample in generator.dataset.samples 
                               if food_item in sample["actual_name"].lower()), None)
            
            if ground_truth:
                total_tests += 1
                
                # Check if correct dish was matched
                is_correct = food_item in result["title"].lower()
                if is_correct:
                    correct_matches += 1
                
                # Calculate ROUGE score
                rouge_score = rouge.score(
                    " ".join(ground_truth["concise_steps"]),
                    " ".join(result["steps"])
                )
                rouge_l = rouge_score['rougeL'].fmeasure
                rouge_scores.append(rouge_l)
                
                # Calculate BLEU score - Fixed
                reference = [[word for step in ground_truth["concise_steps"] 
                            for word in step.split()]]
                candidate = [word for step in result["steps"] 
                           for word in step.split()]
                bleu = sentence_bleu(reference, candidate)
                bleu_scores.append(bleu)
                
                # Print results for this image
                print(f"\nTest image: {Path(test_image).name}")
                print(f"Matched recipe: {result['title']}")
                print(f"Correct match: {'Correct' if is_correct else 'Wrong'}")
                print(f"ROUGE-L score: {rouge_l:.3f}")
                print(f"BLEU score: {bleu:.3f}")
    
    # Print final accuracy metrics
    if total_tests > 0:
        accuracy = correct_matches / total_tests * 100
        avg_rouge = sum(rouge_scores) / len(rouge_scores)
        avg_bleu = sum(bleu_scores) / len(bleu_scores)
        
        print("\nFinal Metrics:")
        print(f"Accuracy: {accuracy:.1f}% ({correct_matches}/{total_tests} correct matches)")
        print(f"Average ROUGE-L score: {avg_rouge:.3f}")
        print(f"Average BLEU score: {avg_bleu:.3f}")

if __name__ == "__main__":
    evaluate_all_test_images()