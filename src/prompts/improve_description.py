"""
Este es el prompt, ya explicado en el notebook, que hydrata la descripción del producto
Utilizando una tecnica de "cadena de pensamiento automatica"
"""

from src.oai import Prompt


system = """
Given the following product features <title>, <description>, <attributes> and <catogory> and the product' images,
make a new and description of the product, highlighting the most relevant and interesting information.
It is important take in account this description will be used for feeding recommender systems.

You must respond in the following way-

<reasoning>
In this section you understand the problem and solve the following plan.

Plan:
1. Read and understand the description
2. Understand attributes
    a. Discards attributes that do not provide information 
    b. Think how they can enhance the description
3. Identify the target audience based on <category>
4. Define the right style and tone for the product and the target audience
5. Describe the images if any
</reasoning>

<description>
Based on the above reasoning, write a new description of the product in this section.
The description MUST be in spanish
</description>
""".strip()


class ImproveDescriptionPrompt(Prompt):

    def __init__(self, title, description, attributes, category, images):
        instruction = f"<title>{title}</title>\n\n<description>\n{description}\n</description>\n\n<category>\n{category}\n</category>\n\n"
        instruction += "<attributes>\n"
        for k, v in attributes.items():
            instruction += f"{k}: {v}\n"
        instruction += "</attributes>"
        super().__init__(system=system, instruction=instruction, images=images)
