#!/usr/bin/env python3
"""
Simple Perplexity API Client

A straightforward script to communicate with the Perplexity AI API.
"""

import argparse
import json
import os
import requests
from typing import Dict, Any, Optional

def query_perplexity(query: str, api_key: str, model: str = "sonar-deep-research") -> Dict[str, Any]:
    """
    Send a query to the Perplexity API and return the response.
    
    Args:
        query: The question or prompt to send
        api_key: Your Perplexity API key
        model: The model to use (default: sonar-medium-online)
        
    Returns:
        The API response as a dictionary
    """
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": query}]
    }
    
    print(f"Sending request to {url}")
    print(f"Headers: {headers}")
    print(f"Payload: {payload}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response received successfully")
            return result
        else:
            print(f"Error: {response.status_code}")
            print(f"Response text: {response.text}")
            return {"error": response.text}
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {"error": str(e)}

def main():
    """Main function to parse arguments and call the API."""
    parser = argparse.ArgumentParser(description="Simple Perplexity API Client")
    parser.add_argument("--query", type=str, help="The question to ask Perplexity")
    parser.add_argument("--api-key", type=str, help="Your Perplexity API key (or set PERPLEXITY_API_KEY env var)")
    parser.add_argument("--model", type=str, default="sonar-deep-research", 
                        help="Model to use (default: sonar-deep-research, options: sonar-deep-research, sonar-reasoning-pro, sonar-reasoning, sonar-pro, sonar, r1-1776)")
    
    args = parser.parse_args()
    
    # Get API key from args or environment
    api_key = args.api_key or os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        print("Error: API key is required. Provide it with --api-key or set the PERPLEXITY_API_KEY environment variable.")
        return
    
    # Get query from args or prompt user
    query = args.query
    if not query:
        query = input("Enter your question: ")
    
    # Call the API
    response = query_perplexity(query, api_key, args.model)
    
    # Print the response
    if "choices" in response:
        print("\nPerplexity Response:")
        print(response["choices"][0]["message"]["content"])
    else:
        print("\nError in API response:")
        print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
