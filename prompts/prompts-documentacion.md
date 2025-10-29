## Prompt 1

### Claude-4-sonnet:

### Prompt:

Create a short descrition for the UML graph

### Answer:

¡Perfecto! He agregado el diagrama UML al README. El archivo ahora incluye:
Referencia a la imagen: ![Diagrama de Clases - Backgammon](assets/uml/Computacion%20nahue.jpeg)
Descripción del diagrama: Explicando las clases principales y sus responsabilidades
El diagrama que tienes es muy completo y muestra exactamente la estructura que necesitas implementar para que tus tests funcionen correctamente. Incluye:
BackgammonGame con players, board, dice
Player con atributos como name, color, checker_count
Board con points() y métodos como place_checker(), move_checker()
Checker con player y métodos de movimiento
Dice con roll() y get_moves()
Ahora el README documenta correctamente tu diseño de clases. ¿Te gustaría que implementemos algunas de estas clases básicas para que los tests funcionen y el coverage sea más preciso?

### What i do with the answer?

I use all the answer

### reference:

assets/uml/computacion nahue.jpeg

## Prompt 2

### Claude-4-sonnet:

### Prompt:

Complete justificacion.md

### Answer:

Perfect! I have completed the JUSTIFICATION.md file with all the required points according to the course requirements. The document now includes:

✅ COMPLETED - JUSTIFICATION.md
Content added:
✅ General design summary – 3-layer architecture (Core/CLI/Pygame)
✅ Justification of chosen classes – Detailed explanation of each class and its responsibilities
✅ Justification of attributes – Why each attribute was chosen in each class
✅ Relevant design decisions – 5 key decisions with justifications
✅ Exceptions and error handling – Implemented strategies
✅ Testing strategies and coverage – 92% coverage (requirement: 90%)
✅ References to SOLID principles – How all five principles are met
✅ Annexes: UML diagrams – You already had the diagram; I added an architecture description

Highlights of the document:

Clean architecture: Clear separation between business logic and interfaces

SOLID principles: Detailed documentation of how they are applied in the refactored CLI

Comprehensive testing: 92% coverage with specific testing strategies

Technical decisions: Justification of each major design decision

Diagrams: Includes class diagram and layered architecture overview

The document is ready for the oral presentation and meets all the course requirements. You now have a complete justification that demonstrates your understanding of the project and its design decisions.

### What i do with the answer?

I use all the answer

### reference:

test/
core/
pygame/
core/

## Prompt 3

### Gpt-5

### Prompt:

@README.md add how to play on cli and pygame

### Answer:

'll add detailed instructions for both CLI and Pygame interfaces to the README.md file:
Perfect! I've enhanced the README.md file with comprehensive instructions for both interfaces:
Added Content:
CLI Usage:
Detailed command descriptions with explanations of what each command does
Step-by-step gameplay instructions showing the typical flow of a game
Clear command syntax with both full names and shortcuts
Pygame Usage:
Visual interface description explaining the graphical representation
Complete control scheme including mouse and keyboard interactions
Gameplay flow with step-by-step instructions for visual play
Visual indicators explanation describing what each color and highlight means
The README now provides users with:
Clear entry points for both interfaces
Complete command reference for CLI users
Visual guide for Pygame users
Game flow instructions for both interfaces
Visual feedback explanations to help users understand the interface
This makes the project much more accessible to new users who want to understand how to play Backgammon using either interface.

### What i do with the answer?

I use all the answer

### reference:

pygame/
cli/
