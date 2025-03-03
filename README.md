# Perplexity API Client

A Python application to communicate with the Perplexity AI API, featuring both a command-line interface and a Flask web application.

## Prerequisites

- Python 3.6 or higher
- A Perplexity API key (get one from [Perplexity AI](https://www.perplexity.ai/settings/api))

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Features

- Command-line interface for quick queries
- Flask web application with:
  - User-friendly search interface
  - Model selection
  - Search history tracking
  - Ability to select and save interesting results
  - "Next stage" processing for selected items

## Usage

### Web Interface

Run the Flask application:

```bash
python app.py
```

Then open your browser and navigate to http://127.0.0.1:5000/

### Command-line Interface

#### Setting up your API key

You can provide your API key in two ways:

1. As a command-line argument:
```bash
python perplexity_client.py --api-key "your-api-key-here" --query "What is quantum computing?"
```

2. As an environment variable:
```bash
# On Windows
set PERPLEXITY_API_KEY=YOUR_API_KEY
# On macOS/Linux
export PERPLEXITY_API_KEY=your-api-key-here

# Then run the script
python perplexity_client.py --query "What is quantum computing?"
```

### Basic Usage

Ask a question:
```bash
python perplexity_client.py --query "What is the capital of France?"
```

If you don't provide a query, the script will prompt you to enter one:
```bash
python perplexity_client.py
# You'll be prompted: "Enter your question: "
```

### Selecting a Model

You can specify which Perplexity model to use:
```bash
python perplexity_client.py --query "Explain quantum physics" --model "pplx-7b-online"
```

Available models include:
- sonar-deep-research (128k) - default
- sonar-reasoning-pro (128k)
- sonar-reasoning (128k)
- sonar-pro (200k)
- sonar (128k)
- r1-1776 (128k)

## Response Format

The script will display the text response from Perplexity AI. If there's an error, it will show the error details.

## Example

```
$ python perplexity_client.py --query "What is machine learning?"

Perplexity Response:
Machine learning is a branch of artificial intelligence (AI) that focuses on building systems that can learn from and make decisions based on data. Instead of being explicitly programmed to perform a task, these systems are trained using algorithms that allow them to identify patterns in data and improve their performance over time through experience.

The core concept of machine learning involves:

1. **Data Collection**: Gathering relevant information for the system to learn from.
2. **Training**: Using algorithms to analyze the data and identify patterns.
3. **Prediction/Decision Making**: Applying what was learned to new, unseen data.
4. **Evaluation and Refinement**: Assessing performance and improving the model.

There are several types of machine learning approaches:

- **Supervised Learning**: The algorithm is trained on labeled data, meaning the input data comes with the correct output. Examples include classification (identifying categories) and regression (predicting continuous values).

- **Unsupervised Learning**: The algorithm works with unlabeled data and must find patterns and relationships on its own. Clustering and dimensionality reduction are common applications.

- **Reinforcement Learning**: The algorithm learns by interacting with an environment and receiving feedback in the form of rewards or penalties.

- **Deep Learning**: A subset of machine learning that uses neural networks with multiple layers (deep neural networks) to analyze various factors of data.

Machine learning has numerous applications across industries, including:
- Image and speech recognition
- Natural language processing
- Recommendation systems
- Fraud detection
- Medical diagnosis
- Autonomous vehicles
- Financial market analysis

As technology advances, machine learning continues to evolve, enabling more sophisticated applications and solutions to complex problems.
