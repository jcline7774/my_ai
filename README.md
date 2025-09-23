MY-AI Chat Interface

A multi-provider AI chat service with web interface, deployed on AWS Lightsail.

Features

**Multiple AI Providers**: Groq (free), DeepSeek (free), OpenRouter (paid)
**Web Chat Interface**: Clean, responsive UI with real-time chat
**Configurable Parameters**: Temperature slider (0-1), token limits, provider selection
**Docker Containerized**: Easy deployment and scaling
**AWS Lightsail Ready**: Production deployment configuration

Live Demo

🚀 **[Try it live](https://my-ai-tiger.1g77wttcjvvnt.us-east-1.cs.amazonlightsail.com)**

API Usage

Generate Response
```bash
curl -X POST "https://my-ai-tiger.1g77wttcjvvnt.us-east-1.cs.amazonlightsail.com/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello, how are you?"}'
```

Use Different Providers
```bash
# DeepSeek (free)
curl -X POST "https://your-domain.com/generate" \
  -H "Content-Type: application/json" \
  -H "X-Provider: deepseek" \
  -d '{"prompt":"Explain quantum computing"}'

# OpenRouter (paid)
curl -X POST "https://your-domain.com/generate" \
  -H "Content-Type: application/json" \
  -H "X-Provider: openrouter" \
  -d '{"prompt":"Write a story", "max_tokens":1000, "temperature":0.8}'
```

Local Development

Prerequisites
- Docker
- Python 3.11+
- API keys for your chosen providers

Setup
1. Clone the repository:
```bash
git clone https://github.com/jcline7774/my-ai-chat.git
cd my-ai-chat
```

2. Create a `.env` file:
```env
GROQ_API_KEY=your_groq_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
```

3. Run locally:
```bash
With Docker
docker build -t my-ai .
docker run -p 8080:8080 --env-file .env my-ai

Or with Python
pip install -r requirements.txt
python app.py
```

4. Open http://localhost:8080

Deployment

AWS Lightsail
1. Build and push Docker image:
```bash
docker build --platform linux/amd64 -t your-username/my-ai:latest .
docker push your-username/my-ai:latest
```

2. Update `deployment-simple.json` with your image and API keys

3. Deploy:
```bash
aws lightsail create-container-service --service-name my-ai --power micro --scale 1
aws lightsail create-container-service-deployment --service-name my-ai --cli-input-json file://deployment-simple.json
```

Configuration

Environment Variables
`GROQ_API_KEY`: Groq API key (get from https://console.groq.com)
`DEEPSEEK_API_KEY`: DeepSeek API key (get from https://platform.deepseek.com)
`OPENROUTER_API_KEY`: OpenRouter API key (get from https://openrouter.ai)
`PORT`: Server port (default: 8080)

Models
**Groq**: `llama-3.1-8b-instant` (free, fast)
**DeepSeek**: `deepseek-chat` (free, good reasoning)
**OpenRouter**: `meta-llama/llama-3.2-1b-instruct` (cheap)

API Reference

POST /generate
Generate AI response

Parameters:
`prompt` (string): User message
`messages` (array): Chat history (optional)
`max_tokens` (int): Response length limit (50-2000)
`temperature` (float): Creativity level (0.0-1.0)
`model` (string): Override default model

Headers:
- `X-Provider`: Choose provider (`groq`, `deepseek`, `openrouter`)

Response:
```json
{
  "response": "AI generated response",
  "raw": { /* Full API response */ }
}
```

Tech Stack

**Backend**: Python Flask
**Frontend**: Vanilla HTML/CSS/JavaScript
**Containerization**: Docker
**Deployment**: AWS Lightsail
**AI Providers**: Groq, DeepSeek, OpenRouter

Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

License

© 2025 White Cloud Technology, concept by John Cline

Contact

- GitHub: [@jcline7774](https://github.com/jcline7774)
- LinkedIn: [jmcline1](https://linkedin.com/in/jmcline1)
- Email: john7774@icloud.com
