# LK Automation - Lead Speech Generator

This project generates personalized speeches for leads using LLM APIs (OpenAI or Deepseek).

## Features

- **Personalized Speech Generation**: Creates custom messages for each lead based on their profile
- **DISC Profile Integration**: Tailors messages according to DISC type and archetype
- **Multiple LLM Support**: Compatible with OpenAI and Deepseek APIs
- **Comprehensive Metadata Tracking**: Records tokens used, timestamps, model info, and status
- **Error Handling**: Automatic retry logic and detailed error logging
- **CSV Processing**: Reads input CSV and generates enriched output with speech data

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure API keys:
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_key_here
# OR
DEEPSEEK_API_KEY=your_deepseek_key_here
```

3. Prepare your input CSV:
Place your `hubspot_lead_automation_import.csv` file in the project root with the following columns:
- First_Name
- Last_Name
- company_name
- job_title
- disc_type
- archetype

## Usage

Run the speech generator:
```bash
python generate_speeches.py
```

The script will:
1. Read leads from `hubspot_lead_automation_import.csv`
2. Generate personalized speeches using the LLM
3. Save results to `hubspot_lead_automation_export_YYYYMMDD_HHMMSS.csv`

## Configuration

You can configure the LLM parameters by editing the script:
- `temperature`: Controls creativity (default: 0.7)
- `max_tokens`: Maximum response length (default: 150)
- `model`: LLM model to use (default: gpt-4 or deepseek-chat)

## Output Format

The output CSV includes all original columns plus:
- `LLM_Generated_Speech`: The generated personalized message
- `LLM_Model`: Model used for generation
- `LLM_Timestamp`: UTC timestamp of generation
- `LLM_Tokens_Used`: Number of tokens consumed
- `LLM_Temperature`: Temperature parameter used
- `LLM_Status`: Success or error status
- `LLM_Error_Log`: Error details (if applicable)

## Success Metrics

- **Generation Rate**: >95% of leads with successfully generated speech
- **Quality**: Coherent and personalized messages
- **Efficiency**: <5 seconds per request (including API latency)

## License

See LICENSE file for details.
