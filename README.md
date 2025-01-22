# Piston: A Genetic Algorithm for Learning to Play Black Jack

## **Status**
🚧 **Works, but needs updates** 🚧

---

## **How It Works**
This application uses a genetic algorithm to train a population of bots to play Black Jack. Here's the process in detail:

1. **Simulation of Gameplay**  
   - The app simulates a population of bots playing Black Jack.  
   - Each bot's actions (e.g., draw or pass) are recorded as genes.

2. **Selection of Best Bots**  
   - The algorithm identifies the top-performing bots—those that lose the least—and selects them for the next generation.

3. **Mutation for Diversity**  
   - One genome (a specific action, such as whether to draw or pass) is mutated in some genes to prevent the population from stagnating.

4. **Reproduction**  
   - The genes of the selected bots are shuffled to create a new population.  
   - The best bots from the previous generation are added to the current generation to prevent regression.

5. **Repetition Until Convergence**  
   - The process repeats until the population stops improving, indicating stagnation.

---

## **Technologies Used**
- **Numpy**: For faster and more efficient handling of lists.  
- **Random**: For shuffling genes and the deck of cards.

---

## **How to Use It**
1. **Clone the Repository**  
   - Use Git to clone the repository or download the `.zip` file from GitHub.

2. **Install Dependencies**  
   - Install the required modules with the following commands:  
     ```bash
     pip install numpy
     pip install random
     ```

3. **Run the Training Script**  
   - Compile and run the `Train_Test.py` file.  
   - Watch the console output to see how the AI improves over time.

---

## **Planned Updates**
- 🌐 **Frontend**: Adding a graphical user interface for better visualization and interaction.  
- 💾 **Genome Persistence**: Implementing functionality to save genomes to a file for future use.

---

Dive in and watch the bots learn to master Black Jack! 🃏
Watch the console output to see how the AI improves over time.
Planned Updates
🌐 Frontend: Adding a graphical user interface for better visualization and interaction.
💾 Genome Persistence: Implementing functionality to save genomes to a file for future use.

It was my first real project that I made so I'm fairly satisfied with it. I hope you'll enjoy using the script and watching the bots improve!
