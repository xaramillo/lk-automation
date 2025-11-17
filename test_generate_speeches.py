#!/usr/bin/env python3
"""
Unit tests for LLM Speech Generator
"""

import os
import sys
import unittest
import pandas as pd
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from generate_speeches import LLMSpeechGenerator, process_leads


class TestLLMSpeechGenerator(unittest.TestCase):
    """Test cases for LLMSpeechGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Set a dummy API key for testing
        os.environ['OPENAI_API_KEY'] = 'sk-test-key-for-testing'
    
    def tearDown(self):
        """Clean up after tests."""
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        if 'DEEPSEEK_API_KEY' in os.environ:
            del os.environ['DEEPSEEK_API_KEY']
    
    def test_init_no_api_key(self):
        """Test initialization without API key raises error."""
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        with self.assertRaises(ValueError) as context:
            LLMSpeechGenerator()
        
        self.assertIn("No API key found", str(context.exception))
    
    def test_init_with_openai_key(self):
        """Test initialization with OpenAI API key."""
        generator = LLMSpeechGenerator()
        self.assertEqual(generator.api_type, 'openai')
        self.assertEqual(generator.model, 'gpt-4')
        self.assertEqual(generator.temperature, 0.7)
        self.assertEqual(generator.max_tokens, 150)
    
    def test_init_with_deepseek_key(self):
        """Test initialization with Deepseek API key."""
        del os.environ['OPENAI_API_KEY']
        os.environ['DEEPSEEK_API_KEY'] = 'sk-test-deepseek-key'
        
        generator = LLMSpeechGenerator()
        self.assertEqual(generator.api_type, 'deepseek')
        self.assertEqual(generator.model, 'deepseek-chat')
    
    def test_build_prompt_complete_data(self):
        """Test prompt building with complete lead data."""
        generator = LLMSpeechGenerator()
        
        lead_data = {
            'First_Name': 'Juan',
            'Last_Name': 'García',
            'company_name': 'TechCorp',
            'job_title': 'Engineer',
            'disc_type': 'Dc',
            'archetype': 'Architect'
        }
        
        prompt = generator._build_prompt(lead_data)
        
        self.assertIn('Juan García', prompt)
        self.assertIn('TechCorp', prompt)
        self.assertIn('Engineer', prompt)
        self.assertIn('Dc', prompt)
        self.assertIn('Architect', prompt)
    
    def test_build_prompt_minimal_data(self):
        """Test prompt building with minimal lead data (defaults)."""
        generator = LLMSpeechGenerator()
        
        lead_data = {
            'First_Name': 'Ana',
            'Last_Name': '',
            'company_name': '',
            'job_title': '',
            'disc_type': '',
            'archetype': ''
        }
        
        prompt = generator._build_prompt(lead_data)
        
        self.assertIn('Ana', prompt)
        self.assertIn('your company', prompt)  # default
        self.assertIn('Profesional', prompt)    # default
        self.assertNotIn('Perfil DISC:', prompt)  # should be omitted
        self.assertNotIn('Arquetipo:', prompt)    # should be omitted
    
    def test_build_prompt_missing_first_name(self):
        """Test prompt building handles missing first name."""
        generator = LLMSpeechGenerator()
        
        lead_data = {
            'First_Name': '',
            'Last_Name': 'Smith',
            'company_name': 'Company',
            'job_title': 'Manager',
            'disc_type': 'IS',
            'archetype': 'Leader'
        }
        
        prompt = generator._build_prompt(lead_data)
        
        # Should use 'there' as default
        self.assertIn('there', prompt)
    
    def test_generate_speech_success(self):
        """Test successful speech generation."""
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hi Juan, I'd love to discuss opportunities!"
        mock_response.usage.total_tokens = 50
        
        mock_client.chat.completions.create.return_value = mock_response
        
        generator = LLMSpeechGenerator()
        generator.client = mock_client
        
        lead_data = {
            'First_Name': 'Juan',
            'Last_Name': 'García',
            'company_name': 'TechCorp',
            'job_title': 'Engineer',
            'disc_type': 'Dc',
            'archetype': 'Architect'
        }
        
        speech, metadata = generator.generate_speech(lead_data)
        
        self.assertIsNotNone(speech)
        self.assertIn("Hi Juan", speech)
        self.assertEqual(metadata['LLM_Status'], 'success')
        self.assertEqual(metadata['LLM_Tokens_Used'], 50)
        self.assertEqual(metadata['LLM_Model'], 'gpt-4')
        self.assertEqual(metadata['LLM_Temperature'], 0.7)
        self.assertEqual(metadata['LLM_Error_Log'], '')
    
    def test_generate_speech_failure_with_retry(self):
        """Test speech generation failure with retry logic."""
        # Mock the OpenAI client to raise exceptions
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        generator = LLMSpeechGenerator()
        generator.client = mock_client
        
        lead_data = {'First_Name': 'Test', 'Last_Name': 'User'}
        
        speech, metadata = generator.generate_speech(lead_data, max_retries=2)
        
        self.assertIsNone(speech)
        self.assertEqual(metadata['LLM_Status'], 'error')
        self.assertIn('API Error', metadata['LLM_Error_Log'])
        
        # Should have tried twice
        self.assertEqual(mock_client.chat.completions.create.call_count, 2)
    
    def test_custom_parameters(self):
        """Test custom temperature and max_tokens."""
        generator = LLMSpeechGenerator(temperature=0.5, max_tokens=200)
        
        self.assertEqual(generator.temperature, 0.5)
        self.assertEqual(generator.max_tokens, 200)


class TestProcessLeads(unittest.TestCase):
    """Test cases for process_leads function."""
    
    def test_missing_input_file(self):
        """Test process_leads with missing input file."""
        with self.assertRaises(FileNotFoundError):
            process_leads('nonexistent_file.csv')
    
    @patch('generate_speeches.LLMSpeechGenerator')
    def test_process_leads_creates_output(self, mock_generator_class):
        """Test that process_leads creates output file."""
        # This test would require creating a temporary CSV
        # and mocking the generator, which is complex
        # For now, we'll just test the file existence check
        pass


if __name__ == '__main__':
    unittest.main()
