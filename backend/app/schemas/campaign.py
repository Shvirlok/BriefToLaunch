from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal, Optional, Any

class CampaignRequest(BaseModel):
    raw_brief: str
    cynicism_level: Literal["realistic", "hardcore", "ruthless"]
    total_budget_usd: int = Field(default=50000, description="Total campaign budget in USD")
    custom_allocations: Optional[dict[str, int]] = None

    @field_validator("custom_allocations")
    @classmethod
    def validate_custom_allocations(cls, v: Optional[dict[str, int]]) -> Optional[dict[str, int]]:
        if v is not None:
            allowed_channels = {"HoReCa", "Digital", "Retail", "CSR"}
            for key in v.keys():
                if key not in allowed_channels:
                    raise ValueError(f"Invalid channel name '{key}'. Allowed channels are: {', '.join(allowed_channels)}")
        return v

    @model_validator(mode="after")
    def validate_budget_matching(self) -> "CampaignRequest":
        if self.custom_allocations is not None:
            total_sum = sum(self.custom_allocations.values())
            if total_sum != self.total_budget_usd:
                raise ValueError(
                    f"Custom budget allocations must sum to exactly total_budget_usd ({self.total_budget_usd}), got {total_sum}"
                )
        return self

class CampaignMeta(BaseModel):
    brand_name: str = Field(description="Name of the brand from the brief")
    target_audience_analysis: str = Field(description="Deep, realistic, and cynical behavioral analysis of the consumer target")
    total_budget_usd: int = Field(description="Total campaign budget in USD")

class ChannelAllocation(BaseModel):
    channel_name: str = Field(description="Name of the channel: HoReCa, Digital, Retail, or CSR")
    allocation_percentage: int = Field(description="Percentage of budget allocated to this channel")
    allocation_budget_usd: int = Field(description="Calculated budget in USD for this specific channel")
    core_strategy: str = Field(description="Ruthless elite positioning strategy for this channel")
    activations: list[str] = Field(description="List of specific, high-end premium activations")
    kpis: list[str] = Field(description="List of strictly measurable, non-fluffy conversion or placement KPIs")

class B2BPitch(BaseModel):
    partner_name: str = Field(description="Name of the extracted strategic partner, retail chain, venue, or NGO")
    target_role: str = Field(description="Job title/role of the decision-maker (e.g. category buyer, executive director)")
    pitch_text: str = Field(description="Aggressive, high-margin commercial proposal tailored to this stakeholder")

class FinancialStressTest(BaseModel):
    risk_score: int = Field(description="A cynical risk rating score from 0 to 100 assessing structural viability")
    burn_rate_verdict: str = Field(description="CMO's biting verdict on capital consumption and allocation speeds")
    estimated_roi_multiplier: float = Field(description="Realistic, highly deflated return multiplier calculated on cold math")
    margin_leak_percentage: int = Field(description="Exact percentage of the budget wasted on hidden agency commissions, inefficient B2B discounts, or logistical friction")

class CampaignResponse(BaseModel):
    campaign_meta: CampaignMeta
    channels: list[ChannelAllocation]
    cmo_verdict: str = Field(description="A sharp, cynical 2-3 sentence final strategic verdict from the CMO")
    b2b_pitches: list[B2BPitch] = Field(description="List of dynamic commercial pitches to key B2B stakeholders")
    financial_stress_test: FinancialStressTest = Field(description="CMO financial stress test report details")

    @model_validator(mode="after")
    def validate_totals(self) -> "CampaignResponse":
        if self.channels:
            total_percentage = sum(ch.allocation_percentage for ch in self.channels)
            total_budget = sum(ch.allocation_budget_usd for ch in self.channels)
            
            if total_percentage != 100:
                raise ValueError(f"Allocation percentages must sum to exactly 100%, got {total_percentage}%")
            
            expected_total = self.campaign_meta.total_budget_usd
            if total_budget != expected_total:
                raise ValueError(f"Allocation budgets must sum to exactly total_budget_usd ({expected_total}) USD, got {total_budget} USD")
            
            for ch in self.channels:
                expected_ch_budget = int(round(ch.allocation_percentage * expected_total / 100.0))
                # Allow a minor tolerance of $1 due to rounding
                if abs(ch.allocation_budget_usd - expected_ch_budget) > 1:
                    raise ValueError(
                        f"Channel {ch.channel_name} budget ({ch.allocation_budget_usd}) does not match percentage ({ch.allocation_percentage}%) of total budget {expected_total}"
                    )
        return self

class ChatMessage(BaseModel):
    sender: Literal["buyer", "user"]
    text: str

class NegotiationRequest(BaseModel):
    strategy_context: dict
    chat_history: list[ChatMessage]
    user_message: str

class NegotiationResponse(BaseModel):
    buyer_response: str = Field(description="The difficult, margin-obsessed buyer's response to the user's counter-argument")
    deal_probability: int = Field(description="The current probability of closing the deal, from 0 to 100")
    criticism_point: str = Field(description="The buyer's main current objection or critical feedback point")
