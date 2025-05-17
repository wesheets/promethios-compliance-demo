"""
OpenAI Integration Module for Conversational Explainability

This module provides integration with OpenAI's API to generate natural language
explanations of compliance decisions and recommendations.
"""

import os
import json
import requests
from typing import Dict, Any, List, Optional

class OpenAIExplainer:
    """
    A class that provides conversational explainability for compliance decisions
    using OpenAI's API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI explainer with an API key.
        
        Args:
            api_key: OpenAI API key. If None, will try to load from environment variable.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set it in the environment as OPENAI_API_KEY or pass it to the constructor.")
        
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4"  # Default to GPT-4 for high-quality explanations
        
        # System prompt template for compliance explanations
        self.system_prompt = """
        You are Promethios, an AI assistant specialized in explaining financial compliance decisions.
        Your role is to provide clear, accurate explanations about loan application compliance decisions
        based on the provided data. Focus on:
        
        1. Explaining why a decision was made in simple, non-technical language
        2. Highlighting the key factors that influenced the decision
        3. Explaining regulatory requirements relevant to the decision
        4. Providing context about the compliance framework being applied
        5. Suggesting potential remediation steps when applicable
        
        Keep explanations concise, factual, and helpful. Avoid speculation beyond the provided data.
        """
    
    def explain_decision(self, decision_data: Dict[str, Any], query: str = "") -> str:
        """
        Generate a natural language explanation for a compliance decision.
        
        Args:
            decision_data: Dictionary containing decision data, trust factors, and compliance results
            query: Optional specific question about the decision
            
        Returns:
            A natural language explanation of the decision
        """
        # Format the decision data for the prompt
        decision_context = json.dumps(decision_data, indent=2)
        
        # Prepare the messages for the API call
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Please explain the following compliance decision:\n\n{decision_context}\n\n" + 
             (f"Specifically address this question: {query}" if query else "Provide a clear explanation of why this decision was made.")}
        ]
        
        # Make the API call
        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.3,  # Lower temperature for more consistent, factual responses
                    "max_tokens": 1000
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract the explanation from the response
            explanation = result["choices"][0]["message"]["content"].strip()
            return explanation
            
        except requests.exceptions.RequestException as e:
            # Handle API errors gracefully
            error_msg = f"Error generating explanation: {str(e)}"
            return error_msg
    
    def generate_recommendations(self, application_data: Dict[str, Any], trust_factors: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate actionable recommendations based on application data and trust factors.
        
        Args:
            application_data: Dictionary containing loan application data
            trust_factors: Dictionary containing trust factor scores and details
            
        Returns:
            A list of recommendation dictionaries with 'title', 'description', and 'priority' keys
        """
        # Format the input data for the prompt
        context = {
            "application": application_data,
            "trust_factors": trust_factors
        }
        context_str = json.dumps(context, indent=2)
        
        # Prepare the messages for the API call
        messages = [
            {"role": "system", "content": """
            You are Promethios, an AI assistant specialized in providing recommendations for improving
            compliance with financial regulations. Based on the provided application data and trust factors,
            generate actionable recommendations to improve compliance. Each recommendation should include
            a title, detailed description, and priority level (high, medium, or low).
            
            Format your response as a JSON array of recommendation objects, each with 'title', 'description',
            and 'priority' fields. Focus on practical, specific actions that would improve compliance scores.
            """},
            {"role": "user", "content": f"Generate recommendations based on this data:\n\n{context_str}"}
        ]
        
        # Make the API call
        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 1000,
                    "response_format": {"type": "json_object"}  # Request JSON format
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract and parse the recommendations
            recommendations_text = result["choices"][0]["message"]["content"].strip()
            recommendations = json.loads(recommendations_text)
            
            # Ensure we have a list of recommendations
            if isinstance(recommendations, dict) and "recommendations" in recommendations:
                return recommendations["recommendations"]
            elif isinstance(recommendations, list):
                return recommendations
            else:
                return []
                
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            # Handle API or parsing errors gracefully
            print(f"Error generating recommendations: {str(e)}")
            return [{"title": "Error generating recommendations", 
                    "description": f"An error occurred: {str(e)}", 
                    "priority": "high"}]
