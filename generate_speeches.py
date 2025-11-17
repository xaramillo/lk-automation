#!/usr/bin/env python3
"""
LLM Speech Generator for Lead Automation

This script generates personalized speeches for leads using LLM APIs (OpenAI/Deepseek).
It reads lead data from a CSV file, generates custom messages, and exports results with metadata.
"""

import os
import sys
import time
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMSpeechGenerator:
    """Generates personalized speeches using LLM APIs."""
    
    def __init__(self, temperature: float = 0.7, max_tokens: int = 150):
        """
        Initialize the speech generator.
        
        Args:
            temperature: Controls creativity/randomness (0.0-1.0)
            max_tokens: Maximum length of generated response
        """
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        
        # Determine which API to use
        if self.openai_api_key:
            self.api_type = 'openai'
            self.model = 'gpt-4'
            self._init_openai()
        elif self.deepseek_api_key:
            self.api_type = 'deepseek'
            self.model = 'deepseek-chat'
            self._init_deepseek()
        else:
            raise ValueError(
                "No API key found. Please set OPENAI_API_KEY or DEEPSEEK_API_KEY in .env file"
            )
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.openai_api_key)
        except ImportError:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
    
    def _init_deepseek(self):
        """Initialize Deepseek client (using OpenAI-compatible API)."""
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.deepseek_api_key,
                base_url="https://api.deepseek.com"
            )
        except ImportError:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
    
    def _build_prompt(self, lead_data: Dict[str, str]) -> str:
        """
        Build a personalized prompt for the LLM.
        
        Args:
            lead_data: Dictionary containing lead information
            
        Returns:
            Formatted prompt string
        """
        first_name = lead_data.get('First_Name', '').strip() or 'there'
        last_name = lead_data.get('Last_Name', '').strip()
        company_name = lead_data.get('company_name', '').strip() or 'your company'
        job_title = lead_data.get('job_title', '').strip() or 'Profesional'
        disc_type = lead_data.get('disc_type', '').strip()
        archetype = lead_data.get('archetype', '').strip()
        
        full_name = f"{first_name} {last_name}".strip() if last_name else first_name
        
        prompt = f"""Genera un mensaje personalizado para {full_name} de {company_name}, cuyo puesto es {job_title}."""
        
        if disc_type:
            prompt += f"\nPerfil DISC: {disc_type}."
        if archetype:
            prompt += f" Arquetipo: {archetype}."
        
        prompt += """
Objetivo: Invitar a una conversación sobre oportunidades laborales.
Tono: Profesional, conciso (< 100 palabras).
Incluir:
1. Saludo personalizado.
2. Mención de su experiencia o empresa.
3. Propuesta de conversación breve (ej: 15 minutos).

Responde SOLO con el mensaje, sin introducción ni explicaciones adicionales."""
        
        return prompt
    
    def generate_speech(
        self, 
        lead_data: Dict[str, str], 
        max_retries: int = 3
    ) -> Tuple[Optional[str], Dict[str, any]]:
        """
        Generate a personalized speech for a lead.
        
        Args:
            lead_data: Dictionary containing lead information
            max_retries: Number of retry attempts on failure
            
        Returns:
            Tuple of (generated_speech, metadata_dict)
        """
        prompt = self._build_prompt(lead_data)
        
        metadata = {
            'LLM_Model': self.model,
            'LLM_Timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'LLM_Tokens_Used': 0,
            'LLM_Temperature': self.temperature,
            'LLM_Status': 'error',
            'LLM_Error_Log': ''
        }
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Eres un experto en crear mensajes profesionales personalizados para reclutamiento."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                speech = response.choices[0].message.content.strip()
                
                # Extract token usage
                if hasattr(response, 'usage') and response.usage:
                    metadata['LLM_Tokens_Used'] = response.usage.total_tokens
                
                metadata['LLM_Status'] = 'success'
                metadata['LLM_Error_Log'] = ''
                
                return speech, metadata
                
            except Exception as e:
                error_msg = f"Attempt {attempt + 1}/{max_retries}: {str(e)}"
                metadata['LLM_Error_Log'] = error_msg
                
                if attempt < max_retries - 1:
                    # Wait before retrying (exponential backoff)
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    # Final attempt failed
                    print(f"Failed to generate speech for {lead_data.get('First_Name', 'lead')}: {error_msg}")
                    return None, metadata
        
        return None, metadata


def process_leads(
    input_file: str = 'hubspot_lead_automation_import.csv',
    output_dir: str = '.'
) -> str:
    """
    Process leads from CSV and generate speeches.
    
    Args:
        input_file: Path to input CSV file
        output_dir: Directory to save output file
        
    Returns:
        Path to output CSV file
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Load CSV
    print(f"Loading leads from {input_file}...")
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} leads")
    
    # Initialize generator
    print("Initializing LLM speech generator...")
    generator = LLMSpeechGenerator(temperature=0.7, max_tokens=150)
    print(f"Using {generator.api_type.upper()} API with model: {generator.model}")
    
    # Initialize output columns
    df['LLM_Generated_Speech'] = ''
    df['LLM_Model'] = ''
    df['LLM_Timestamp'] = ''
    df['LLM_Tokens_Used'] = 0
    df['LLM_Temperature'] = 0.0
    df['LLM_Status'] = ''
    df['LLM_Error_Log'] = ''
    
    # Process each lead
    print("\nGenerating speeches...")
    success_count = 0
    
    for idx, row in df.iterrows():
        print(f"Processing lead {idx + 1}/{len(df)}: {row.get('First_Name', 'Unknown')} {row.get('Last_Name', '')}...", end=' ')
        
        lead_data = row.to_dict()
        speech, metadata = generator.generate_speech(lead_data)
        
        if speech:
            df.at[idx, 'LLM_Generated_Speech'] = speech
            success_count += 1
            print("✓")
        else:
            df.at[idx, 'LLM_Generated_Speech'] = ''
            print("✗")
        
        # Update metadata
        df.at[idx, 'LLM_Model'] = metadata['LLM_Model']
        df.at[idx, 'LLM_Timestamp'] = metadata['LLM_Timestamp']
        df.at[idx, 'LLM_Tokens_Used'] = metadata['LLM_Tokens_Used']
        df.at[idx, 'LLM_Temperature'] = metadata['LLM_Temperature']
        df.at[idx, 'LLM_Status'] = metadata['LLM_Status']
        df.at[idx, 'LLM_Error_Log'] = metadata['LLM_Error_Log']
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f'hubspot_lead_automation_export_{timestamp}.csv')
    
    # Save results
    df.to_csv(output_file, index=False)
    
    # Print summary
    success_rate = (success_count / len(df)) * 100 if len(df) > 0 else 0
    print(f"\n{'='*60}")
    print(f"Processing complete!")
    print(f"{'='*60}")
    print(f"Total leads processed: {len(df)}")
    print(f"Successful generations: {success_count}")
    print(f"Failed generations: {len(df) - success_count}")
    print(f"Success rate: {success_rate:.2f}%")
    print(f"Output saved to: {output_file}")
    print(f"{'='*60}")
    
    return output_file


def main():
    """Main entry point."""
    try:
        # Check for input file
        input_file = 'hubspot_lead_automation_import.csv'
        
        if len(sys.argv) > 1:
            input_file = sys.argv[1]
        
        # Process leads
        output_file = process_leads(input_file)
        
        print("\n✓ Speech generation completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
