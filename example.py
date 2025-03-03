#!/usr/bin/env python3
"""
Example usage of the Perplexity API client
"""

import os
from perplexity_client import query_perplexity

def main():
    # Get API key from environment variable
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        print("Please set the PERPLEXITY_API_KEY environment variable")
        return
    
    # Example 1: Basic question
    question = "What are the three laws of thermodynamics?"
    print(f"\nQuestion: {question}")
    
    response = query_perplexity(question, api_key)
    if "choices" in response:
        print("\nAnswer:")
        print(response["choices"][0]["message"]["content"])
    else:
        print("Error:", response)
    
    # Example 2: Using a different model
    question = "Explain the concept of quantum entanglement in simple terms"
    print(f"\nQuestion: {question}")
    
    response = query_perplexity(question, api_key, model="sonar-pro")
    if "choices" in response:
        print("\nAnswer:")
        print(response["choices"][0]["message"]["content"])
    else:
        print("Error:", response)

if __name__ == "__main__":
    main()
