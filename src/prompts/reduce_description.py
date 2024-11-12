"""
Este prompt reduce la descripción del producto a un maximo de n palabras
"""

from src.oai import Prompt


system = """
Reduce the product description to a maximum of {n} words while retaining all relevant information.

# Steps

1. Read the original product description carefully.
2. Identify the key features, benefits, and specifications that are essential to understanding the product.
3. Eliminate any redundant or non-essential information.
4. Rewrite the description concisely, ensuring it does not exceed the word limit of {n} words.

# Output Format
The output should be a single paragraph containing no more than {n} words.

# Examples

**Input:** "This high-quality, durable backpack is perfect for hiking, traveling, and everyday use. It features multiple compartments, water-resistant material, and a comfortable fit for all-day wear."

**Output:** "Durable backpack ideal for hiking and travel, with multiple compartments and water-resistant material."

**Input:** "Our innovative kitchen blender offers powerful blending capabilities, a sleek design, and easy-to-clean components, making it a must-have for any home chef."

**Output:** "Powerful kitchen blender with sleek design and easy-to-clean components, perfect for home chefs."
""".strip()


class ReduceDescriptionPrompt(Prompt):
    def __init__(self, description, n):
        super().__init__(system=system.format(n=n), instruction=description)
