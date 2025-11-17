# Usage Examples

This document provides practical examples of how to use the LLM Speech Generator.

## Basic Usage

### 1. Setup Environment

Create a `.env` file:
```bash
# For OpenAI
OPENAI_API_KEY=sk-your-actual-key-here

# OR for Deepseek
DEEPSEEK_API_KEY=sk-your-actual-key-here
```

### 2. Prepare Input CSV

Your `hubspot_lead_automation_import.csv` should have these columns:

| First_Name | Last_Name | company_name | job_title | disc_type | archetype |
|------------|-----------|--------------|-----------|-----------|-----------|
| Juan | García | TechCorp | Engineer | Dc | Architect |
| María | Rodríguez | InnovateX | Manager | IS | Harmonizer |

### 3. Run the Generator

```bash
python generate_speeches.py
```

### 4. Check Output

The script will create a file like:
```
hubspot_lead_automation_export_20231117_143022.csv
```

## Advanced Usage

### Custom Input File

```bash
python generate_speeches.py path/to/your/custom_file.csv
```

### Using as a Module

```python
from generate_speeches import LLMSpeechGenerator

# Initialize generator
generator = LLMSpeechGenerator(temperature=0.5, max_tokens=200)

# Generate speech for a single lead
lead_data = {
    'First_Name': 'John',
    'Last_Name': 'Doe',
    'company_name': 'Tech Corp',
    'job_title': 'Software Engineer',
    'disc_type': 'Di',
    'archetype': 'Pioneer'
}

speech, metadata = generator.generate_speech(lead_data)

if speech:
    print(f"Generated speech: {speech}")
    print(f"Tokens used: {metadata['LLM_Tokens_Used']}")
else:
    print(f"Failed: {metadata['LLM_Error_Log']}")
```

## Output Format

The output CSV includes all original columns plus:

### Example Output Row

```csv
First_Name,Last_Name,company_name,job_title,disc_type,archetype,LLM_Generated_Speech,LLM_Model,LLM_Timestamp,LLM_Tokens_Used,LLM_Temperature,LLM_Status,LLM_Error_Log
Juan,García,TechCorp,Engineer,Dc,Architect,"Hola Juan, he visto tu perfil en TechCorp y tu rol como Engineer. Me gustaría conversar sobre una oportunidad que podría alinearse con tus objetivos. ¿Te interesaría una llamada de 15 minutos?",gpt-4,2023-11-17T14:30:22.123Z,87,0.7,success,""
```

### Metadata Fields Explained

| Field | Description | Example |
|-------|-------------|---------|
| `LLM_Generated_Speech` | The personalized message | "Hola Juan..." |
| `LLM_Model` | Model used | "gpt-4" |
| `LLM_Timestamp` | UTC timestamp | "2023-11-17T14:30:22Z" |
| `LLM_Tokens_Used` | Tokens consumed | 87 |
| `LLM_Temperature` | Creativity parameter | 0.7 |
| `LLM_Status` | Success or error | "success" |
| `LLM_Error_Log` | Error details (if any) | "" |

## Configuration Options

### Temperature

Controls the creativity/randomness of responses:
- `0.0-0.3`: More focused and deterministic
- `0.4-0.7`: Balanced (default: 0.7)
- `0.8-1.0`: More creative and varied

```python
generator = LLMSpeechGenerator(temperature=0.5)
```

### Max Tokens

Controls the maximum length of generated speech:
- `50-100`: Very short messages
- `100-150`: Standard messages (default: 150)
- `150-300`: Longer, more detailed messages

```python
generator = LLMSpeechGenerator(max_tokens=200)
```

## Error Handling

### Common Errors and Solutions

#### 1. Missing API Key
```
Error: No API key found. Please set OPENAI_API_KEY or DEEPSEEK_API_KEY in .env file
```
**Solution**: Create a `.env` file with your API key.

#### 2. Invalid API Key
```
Error: Attempt 3/3: Incorrect API key provided
```
**Solution**: Verify your API key is correct and active.

#### 3. Rate Limiting
```
Error: Attempt 3/3: Rate limit exceeded
```
**Solution**: Wait a few moments and try again. The script will automatically retry with exponential backoff.

#### 4. Input File Not Found
```
FileNotFoundError: Input file not found: hubspot_lead_automation_import.csv
```
**Solution**: Ensure your CSV file is in the correct location.

## Best Practices

### 1. API Key Security
- Never commit `.env` files to git
- Use environment-specific keys for development/production
- Rotate keys regularly

### 2. Cost Management
- Monitor your API usage in the provider's dashboard
- Start with a small batch to test
- Use appropriate `max_tokens` to avoid waste

### 3. Quality Control
- Review a sample of generated speeches
- Adjust `temperature` if messages are too generic or too random
- Ensure input data is clean and complete

### 4. Performance
- Process in batches if you have many leads
- The script includes automatic retry logic for failures
- Expected: <5 seconds per lead including API latency

## Testing

### Run Demo Without API Calls

```bash
python demo.py
```

This shows how prompts are built without consuming API tokens.

### Run Unit Tests

```bash
python -m unittest test_generate_speeches -v
```

Expected output:
```
Ran 11 tests in 1.5s
OK
```

## Troubleshooting

### Check Dependencies
```bash
pip install -r requirements.txt
```

### Verify Python Version
```bash
python --version
# Should be Python 3.8 or higher
```

### Test CSV Loading
```python
import pandas as pd
df = pd.read_csv('hubspot_lead_automation_import.csv')
print(f"Loaded {len(df)} rows")
print(df.columns)
```

## Support

For issues or questions:
1. Check this documentation first
2. Review the error message carefully
3. Ensure all dependencies are installed
4. Verify API keys are correct
5. Check the API provider's status page

## Example Workflow

Complete workflow from start to finish:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
echo "OPENAI_API_KEY=sk-your-key" > .env

# 3. Verify input CSV exists
ls -l hubspot_lead_automation_import.csv

# 4. Run demo to test (no API calls)
python demo.py

# 5. Run actual generation
python generate_speeches.py

# 6. Check output
ls -l hubspot_lead_automation_export_*.csv

# 7. View results
head -n 2 hubspot_lead_automation_export_*.csv
```
