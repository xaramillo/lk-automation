#!/usr/bin/env python3
"""
Demo script showing how to use the LLM Speech Generator.

This script demonstrates the usage without actually calling the API.
"""

import os
from datetime import datetime, timezone
from generate_speeches import LLMSpeechGenerator


def demo_prompt_generation():
    """Demonstrate prompt generation without calling the API."""
    print("=" * 60)
    print("LLM Speech Generator - Demo")
    print("=" * 60)
    
    # Set a dummy API key to allow initialization
    os.environ['OPENAI_API_KEY'] = 'sk-dummy-key-for-demo'
    
    generator = LLMSpeechGenerator()
    
    # Example lead data
    leads = [
        {
            'First_Name': 'Juan',
            'Last_Name': 'García',
            'company_name': 'TechCorp Solutions',
            'job_title': 'Senior Software Engineer',
            'disc_type': 'Dc',
            'archetype': 'Architect'
        },
        {
            'First_Name': 'María',
            'Last_Name': 'Rodríguez',
            'company_name': 'InnovateX',
            'job_title': 'Product Manager',
            'disc_type': 'IS',
            'archetype': 'Harmonizer'
        },
        {
            'First_Name': 'Ana',
            'Last_Name': '',
            'company_name': '',
            'job_title': '',
            'disc_type': '',
            'archetype': ''
        }
    ]
    
    print("\nDemonstration of prompt generation for different lead profiles:\n")
    
    for i, lead in enumerate(leads, 1):
        print(f"\n{'=' * 60}")
        print(f"Lead {i}: {lead.get('First_Name', 'Unknown')} {lead.get('Last_Name', '')}")
        print(f"{'=' * 60}")
        
        # Build and display prompt
        prompt = generator._build_prompt(lead)
        print("\nGenerated Prompt:")
        print("-" * 60)
        print(prompt)
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print("Demo Configuration:")
    print("=" * 60)
    print(f"API Type: {generator.api_type}")
    print(f"Model: {generator.model}")
    print(f"Temperature: {generator.temperature}")
    print(f"Max Tokens: {generator.max_tokens}")
    
    print("\n" + "=" * 60)
    print("Sample Metadata Output:")
    print("=" * 60)
    sample_metadata = {
        'LLM_Model': generator.model,
        'LLM_Timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'LLM_Tokens_Used': 125,
        'LLM_Temperature': generator.temperature,
        'LLM_Status': 'success',
        'LLM_Error_Log': ''
    }
    for key, value in sample_metadata.items():
        print(f"{key}: {value}")
    
    print("\n" + "=" * 60)
    print("To run the actual speech generation:")
    print("=" * 60)
    print("1. Create a .env file with your API key:")
    print("   OPENAI_API_KEY=your_key_here")
    print("   (or DEEPSEEK_API_KEY=your_key_here)")
    print("\n2. Run: python generate_speeches.py")
    print("\n3. The output will be saved to:")
    print("   hubspot_lead_automation_export_YYYYMMDD_HHMMSS.csv")
    print("=" * 60)


if __name__ == '__main__':
    demo_prompt_generation()
