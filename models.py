from dataclasses import dataclass
from langchain_aws import ChatBedrockConverse

AWS_REGION = "eu-west-2"
AWS_PROFILE = "sandbox"


@dataclass
class ModelConfig:
    model_id: str
    temperature: float
    max_tokens: int


@dataclass
class AWSConfig:
    region_name: str
    credentials_profile_name: str = None


nova_micro_config = ModelConfig(
    model_id="amazon.nova-micro-v1:0", temperature=0.7, max_tokens=4000
)
nova_pro_config = ModelConfig(
    model_id="amazon.nova-pro-v1:0", temperature=0.7, max_tokens=2048
)


def get_bedrock_model(
    model_config: ModelConfig, aws_config: AWSConfig
) -> ChatBedrockConverse:
    return ChatBedrockConverse(
        region_name=aws_config.region_name,
        credentials_profile_name=aws_config.credentials_profile_name,
        model_id=model_config.model_id,
        temperature=model_config.temperature,
        max_tokens=model_config.max_tokens,
    )


aws_config = AWSConfig(region_name=AWS_REGION, credentials_profile_name=AWS_PROFILE)
nova_micro = get_bedrock_model(nova_micro_config, aws_config)
nova_pro = get_bedrock_model(nova_pro_config, aws_config)
