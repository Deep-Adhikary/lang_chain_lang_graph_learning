# LangChain + LangGraph Agent Starter

A small, practical starter for building mood-aware, tool-using conversational agents with LangChain and LangGraph. It includes an interactive console UI, deterministic guardrails for abusive content, dynamic system prompts driven by detected user mood, and example tools that call OpenWeather APIs.

## Features
- Dynamic system prompt: Adapts tone based on detected user mood via `MoodMiddleware`.
- Deterministic guardrail: Denies service for abusive or inappropriate requests (`check_abusive_service`).
- Tool usage: Weather, air quality, and geolocation tools built on OpenWeather APIs.
- Configurable model provider: AWS Bedrock (Nova) for the main chat model; Ollama (Qwen3) for safety classification.
- Simple interactive console: Run the agent locally and chat in your terminal.

## Architecture
- Main agent: constructed in [src/agents/simple_agent.py](src/agents/simple_agent.py)
	- Base model: `base_model` from [src/models.py](src/models.py) using AWS Bedrock.
	- Guardrails: `check_abusive_service` from [src/guardrails/denied_service_abbusive.py](src/guardrails/denied_service_abbusive.py) (Ollama + Qwen3 structured output).
	- Mood: `MoodMiddleware` from [src/states/mood.py](src/states/mood.py) classifies mood and injects state.
	- Dynamic prompt: `user_moode_based_prompt` selects a system message from [src/prompts/system_prompts.py](src/prompts/system_prompts.py) based on mood.
	- Tools: weather/geolocation in [src/tools/weather.py](src/tools/weather.py).
- Interactive console: [src/front_end/interactive_console.py](src/front_end/interactive_console.py) runs a loop and calls `agent.invoke()`.

## Requirements
- Python 3.11 (as enforced by `pyproject.toml`).
- AWS account with Bedrock access in `eu-west-2` (default) and an AWS named profile called `sandbox` (or update the config).
- Ollama installed and running locally with the `qwen3:8b` model (used for the safety classifier).
- OpenWeather API key exported as `WEATHER_API_KEY` for tools.
- macOS/Linux/WSL recommended. Windows works with Python 3.11 and compatible tools installed.

## Setup
1) Create and activate a virtual environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies
```bash
pip install -U pip
pip install -e .
```

3) Configure AWS for Bedrock
```bash
# Ensure an AWS profile named "sandbox" exists and has Bedrock permissions
aws configure --profile sandbox
```
If you use a different profile or region, edit [src/configs/model_configs.py](src/configs/model_configs.py):
- `AWS_REGION` (default `eu-west-2`)
- `AWS_PROFILE` (default `sandbox`)

4) Start Ollama and pull the classifier model
```bash
ollama serve
ollama pull qwen3:8b
```

5) Set your OpenWeather API key
```bash
export WEATHER_API_KEY="your_openweather_api_key"
```

## Quickstart
Run the interactive console (uses the simple agent):
```bash
python -m src.agents.simple_agent
```
Then try:
- "What’s the weather in London?"
- "Give me the air quality for 51.5074, -0.1278"

Type `exit` to quit.

## Configuration
- Model provider (main chat model): controlled in [src/models.py](src/models.py) via `init_chat_model()` and values from [src/configs/model_configs.py](src/configs/model_configs.py).
	- Defaults to AWS Bedrock Converse with Nova models.
	- Preset configs: `nova_micro_config`, `nova_lite_config`, `nova_pro_config`.
	- Change the active preset by editing `base_model` construction in [src/models.py](src/models.py).
- Safety classifier: defined in [src/guardrails/denied_service_abbusive.py](src/guardrails/denied_service_abbusive.py) using Ollama + `qwen3:8b`.
	- Switch to a different local model by changing `qwen_3_config` in [src/configs/model_configs.py](src/configs/model_configs.py).
- Mood detection: implemented in [src/states/mood.py](src/states/mood.py), returns a small dict with `user_mood` and `reason`.
- System prompts: see [src/prompts/system_prompts.py](src/prompts/system_prompts.py) and adjust content/tones.
- Tools: see [src/tools/weather.py](src/tools/weather.py) and add your own with `@tool`.

## Project Structure
```
src/
	agents/
		simple_agent.py         # Assembles the agent: model, guardrails, mood, tools
	configs/
		model_configs.py        # AWS/Ollama configs and model presets
	front_end/
		interactive_console.py  # Minimal terminal UI
	guardrails/
		denied_service_abbusive.py # Abusive content guardrail (Ollama + Qwen3)
	prompts/
		system_prompts.py       # System prompt variants (mood-based)
		abusive_checker_prompt.py# Safety-classifier prompt
	states/
		mood.py                 # Mood detection middleware/state
	tools/
		weather.py              # OpenWeather tools (geo/weather/air quality)
models.py                   # Base model init (AWS Bedrock)
```

## Extending
- Add a tool: create a function in `src/tools/` and decorate with `@tool`, then include it in the `tools=[...]` list in `simple_agent.py`.
- Add a guardrail: implement a `@before_agent` middleware and include it in `middleware=[...]`.
- Add a mood/state: create an `AgentMiddleware` subclass and register it.
- Tweak tone: update system prompts in `src/prompts/` or extend the dynamic selector.

## Notebooks & Archive
- Exploration and deep-dives live under `archive/`:
	- [archive/agent_deep_dive.py](archive/agent_deep_dive.py)
	- [archive/langchain-quickstart.ipynb](archive/langchain-quickstart.ipynb)
	- [archive/model_deep_dive.ipynb](archive/model_deep_dive.ipynb)
These are illustrative and not required to run the main app.

## Troubleshooting
- Bedrock errors: ensure your AWS profile has Bedrock permissions and region matches `AWS_REGION`.
- Ollama model errors: verify `ollama serve` is running and `ollama pull qwen3:8b` was successful.
- OpenWeather 401/403: confirm `WEATHER_API_KEY` is set and valid.
- Python version: use Python 3.11; mismatches can cause install/runtime issues.

## Scripts and Commands Cheat‑Sheet
```bash
# Create venv and install
python3.11 -m venv .venv && source .venv/bin/activate
pip install -U pip && pip install -e .

# Environment
export WEATHER_API_KEY="your_openweather_api_key"
aws configure --profile sandbox
ollama serve &
ollama pull qwen3:8b

# Run console
python -m src.agents.simple_agent
```

## License
No license declared yet. Consider adding a LICENSE file (e.g., MIT or Apache-2.0).

