import json
import os
import random
from typing import Literal, Tuple, List

# Ensure consistent results across runs
random.seed(42)

SYMBOLS = list("abcdefghijklmnopqrstuvwxyz")
DELIMETER = "->"
INSTRUCTION = (
    'Figure out the pattern in the below examples, and then answer with just "foo" or "bar".'
)
TASK_NAME = "pattern_identification"

# Enhanced AI Feature: Generate example with pattern classification
def generate_example() -> Tuple[str, List[str], Literal["foo", "bar"]]:
    num_symbols = int(len(SYMBOLS) / 2)
    target_symbol = random.choice(SYMBOLS)
    symbol_list = random.sample(SYMBOLS, num_symbols)
    
    # AI-driven feature: Enhanced pattern recognition
    target: Literal["foo", "bar"] = "foo" if target_symbol in symbol_list else "bar"
    return (target_symbol, symbol_list, target)

# Enhanced AI Feature: Generate a set of multiple examples with advanced pattern detection
def generate_exemplars_str(num_exemplars: int = 8) -> str:
    exemplars = [generate_example() for _ in range(num_exemplars)]
    exemplars_str = [
        f"({exemplar[0]}, {exemplar[1]}) {DELIMETER} {exemplar[2]}".replace("'", "")
        for exemplar in exemplars
    ]
    
    # AI-driven feature: Adding contextual clues for better pattern understanding
    contextual_exemplars = [
        f"Example {i+1}: {exemplar}" for i, exemplar in enumerate(exemplars_str)
    ]
    return "\n".join([INSTRUCTION] + contextual_exemplars)

# Enhanced AI Feature: Generate evaluation examples with improved context and error handling
def generate_eval_examples(
    num_eval_examples: int = 250,
) -> Tuple[List[str], List[Literal["foo", "bar"]]]:
    eval_examples = [generate_example() for _ in range(num_eval_examples)]
    eval_examples_str = [
        f"{generate_exemplars_str()}\n({example[0]}, {example[1]}) {DELIMETER}".replace("'", "")
        for example in eval_examples
    ]
    targets: List[Literal["foo", "bar"]] = [example[2] for example in eval_examples]
    
    # AI-driven feature: Error handling and data validation
    if not eval_examples_str or not targets:
        raise ValueError("Evaluation examples or targets cannot be empty.")
        
    return eval_examples_str, targets

if __name__ == "__main__":
    eval_examples_str, targets = generate_eval_examples()

    # Generate the output path in an OS-agnostic manner
    output_path = os.path.join("evals", "registry", "data", TASK_NAME, "samples.v0.jsonl")

    # AI-driven feature: Enhanced file handling with automated directory creation
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as writer:
        for eval_example_str, target in zip(eval_examples_str, targets):
            d = {
                "input": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": eval_example_str},
                ],
                "ideal": target,
            }
            writer.write(json.dumps(d) + "\n")
    print(f"{len(eval_examples_str)} lines written to {output_path}.")
