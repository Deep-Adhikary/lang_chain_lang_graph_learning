from dataclasses import dataclass

AWS_REGION = "eu-west-2"
AWS_PROFILE = "sandbox"


@dataclass
class ModelConfig:
    model: str
    temperature: float
    max_tokens: int


@dataclass
class AWSConfig:
    model_provider: str = "bedrock_converse"
    region_name: str = AWS_REGION
    credentials_profile_name: str = AWS_PROFILE


@dataclass
class OllamaConfig:
    model_provider: str = "ollama"


nova_micro_config = ModelConfig(model="amazon.nova-micro-v1:0", temperature=0, max_tokens=4000)
nova_lite_config = ModelConfig(model="amazon.nova-lite-v1:0", temperature=0, max_tokens=8192)
nova_pro_config = ModelConfig(model="amazon.nova-pro-v1:0", temperature=0, max_tokens=2048)
qwen_3_config = ModelConfig(model="qwen3:8b", temperature=0, max_tokens=32768)
