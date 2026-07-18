import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from app.main import app
from app.services.llm import LLMService
from app.schemas.campaign import CampaignResponse, CampaignMeta, ChannelAllocation, CampaignRequest, B2BPitch, FinancialStressTest

def test_campaign_request_valid():
    req = CampaignRequest(raw_brief="Test brief content", cynicism_level="realistic")
    assert req.raw_brief == "Test brief content"
    assert req.cynicism_level == "realistic"
    assert req.custom_allocations is None

def test_campaign_request_invalid_cynicism_level():
    with pytest.raises(ValidationError) as exc_info:
        CampaignRequest(raw_brief="Test brief content", cynicism_level="Fluffy")  # type: ignore
    assert "cynicism_level" in str(exc_info.value)

def test_campaign_request_valid_custom_allocations():
    req = CampaignRequest(
        raw_brief="Test brief content",
        cynicism_level="ruthless",
        total_budget_usd=1500000,
        custom_allocations={
            "Digital": 900000,
            "HoReCa": 600000
        }
    )
    assert req.custom_allocations["Digital"] == 900000
    assert req.custom_allocations["HoReCa"] == 600000

def test_campaign_request_invalid_custom_allocations_sum():
    with pytest.raises(ValidationError) as exc_info:
        CampaignRequest(
            raw_brief="Test brief content",
            cynicism_level="ruthless",
            total_budget_usd=1500000,
            custom_allocations={
                "Digital": 800000,
                "HoReCa": 600000
            }  # Sum is 1400000, must be 1500000
        )
    assert "Custom budget allocations must sum to exactly total_budget_usd" in str(exc_info.value)

def test_campaign_request_invalid_custom_allocations_channel():
    with pytest.raises(ValidationError) as exc_info:
        CampaignRequest(
            raw_brief="Test brief content",
            cynicism_level="ruthless",
            total_budget_usd=1500000,
            custom_allocations={
                "Billboard": 1500000  # Invalid channel name
            }
        )
    assert "Invalid channel name 'Billboard'" in str(exc_info.value)

def test_campaign_response_validation_success():
    data = {
        "campaign_meta": {
            "brand_name": "Test Brand",
            "target_audience_analysis": "Cynical profile",
            "total_budget_usd": 1500000
        },
        "channels": [
            {
                "channel_name": "Digital",
                "allocation_percentage": 60,
                "allocation_budget_usd": 900000,
                "core_strategy": "Digital placement",
                "activations": ["Ad placement"],
                "kpis": ["CTR"]
            },
            {
                "channel_name": "HoReCa",
                "allocation_percentage": 40,
                "allocation_budget_usd": 600000,
                "core_strategy": "Bar activations",
                "activations": ["Bar stand"],
                "kpis": ["Footfall"]
            }
        ],
        "cmo_verdict": "A biting CMO verdict.",
        "b2b_pitches": [
            {
                "partner_name": "Goodwine",
                "target_role": "Buyer",
                "pitch_text": "Goodwine pitch content."
            }
        ],
        "financial_stress_test": {
            "risk_score": 45,
            "burn_rate_verdict": "Verdict text.",
            "estimated_roi_multiplier": 1.5,
            "margin_leak_percentage": 18
        }
    }
    
    response = CampaignResponse(**data)
    assert response.campaign_meta.brand_name == "Test Brand"
    assert len(response.channels) == 2
    assert response.b2b_pitches[0].partner_name == "Goodwine"
    assert response.financial_stress_test.risk_score == 45

def test_campaign_response_invalid_budget():
    data = {
        "campaign_meta": {
            "brand_name": "Test Brand",
            "target_audience_analysis": "Cynical profile",
            "total_budget_usd": 1000000  # Invalid, expected sum of channels (1,500,000)
        },
        "channels": [
            {
                "channel_name": "Digital",
                "allocation_percentage": 100,
                "allocation_budget_usd": 1500000,
                "core_strategy": "Digital placement",
                "activations": ["Ad placement"],
                "kpis": ["CTR"]
            }
        ],
        "cmo_verdict": "Verdict",
        "b2b_pitches": [],
        "financial_stress_test": {
            "risk_score": 45,
            "burn_rate_verdict": "Verdict text.",
            "estimated_roi_multiplier": 1.5,
            "margin_leak_percentage": 18
        }
    }
    with pytest.raises(ValidationError) as exc_info:
        CampaignResponse(**data)
    assert "Allocation budgets must sum to exactly total_budget_usd" in str(exc_info.value)

def test_campaign_response_invalid_percentages():
    data = {
        "campaign_meta": {
            "brand_name": "Test Brand",
            "target_audience_analysis": "Cynical profile",
            "total_budget_usd": 1500000
        },
        "channels": [
            {
                "channel_name": "Digital",
                "allocation_percentage": 50,  # 50% * 15000 = 750000
                "allocation_budget_usd": 750000,
                "core_strategy": "Strategy",
                "activations": ["Activation"],
                "kpis": ["KPI"]
            },
            {
                "channel_name": "HoReCa",
                "allocation_percentage": 40,  # 40% * 15000 = 600000
                "allocation_budget_usd": 600000,
                "core_strategy": "Strategy",
                "activations": ["Activation"],
                "kpis": ["KPI"]
            }
        ],  # Total percentage = 90% (Invalid, must be 100%)
        "cmo_verdict": "Verdict",
        "b2b_pitches": [],
        "financial_stress_test": {
            "risk_score": 45,
            "burn_rate_verdict": "Verdict text.",
            "estimated_roi_multiplier": 1.5,
            "margin_leak_percentage": 18
        }
    }
    with pytest.raises(ValidationError) as exc_info:
        CampaignResponse(**data)
    assert "Allocation percentages must sum to exactly 100%" in str(exc_info.value)

def test_campaign_response_mismatched_channel_budget():
    data = {
        "campaign_meta": {
            "brand_name": "Test Brand",
            "target_audience_analysis": "Cynical profile",
            "total_budget_usd": 1500000
        },
        "channels": [
            {
                "channel_name": "Digital",
                "allocation_percentage": 60,
                "allocation_budget_usd": 800000,  # Expected 900000 (60 * 15000)
                "core_strategy": "Strategy",
                "activations": ["Activation"],
                "kpis": ["KPI"]
            },
            {
                "channel_name": "HoReCa",
                "allocation_percentage": 40,
                "allocation_budget_usd": 700000,  # Expected 600000 (40 * 15000)
                "core_strategy": "Strategy",
                "activations": ["Activation"],
                "kpis": ["KPI"]
            }
        ],
        "cmo_verdict": "Verdict",
        "b2b_pitches": [],
        "financial_stress_test": {
            "risk_score": 45,
            "burn_rate_verdict": "Verdict text.",
            "estimated_roi_multiplier": 1.5,
            "margin_leak_percentage": 18
        }
    }
    with pytest.raises(ValidationError) as exc_info:
        CampaignResponse(**data)
    assert "does not match percentage" in str(exc_info.value)

class MockLLMService:
    async def generate_structured_strategy(self, request: CampaignRequest) -> CampaignResponse:
        data = {
            "campaign_meta": {
                "brand_name": "Mock Brand",
                "target_audience_analysis": "Cynical profile",
                "total_budget_usd": request.total_budget_usd
            },
            "channels": [
                {
                    "channel_name": "Digital",
                    "allocation_percentage": 100,
                    "allocation_budget_usd": request.total_budget_usd,
                    "core_strategy": "Digital placement",
                    "activations": ["Ad placement"],
                    "kpis": ["CTR"]
                }
            ],
            "cmo_verdict": f"A biting CMO verdict. Cynicism Level: {request.cynicism_level}",
            "b2b_pitches": [
                {
                    "partner_name": "Mock Partner",
                    "target_role": "Mock Buyer",
                    "pitch_text": "Mock pitch content."
                }
            ],
            "financial_stress_test": {
                "risk_score": 33,
                "burn_rate_verdict": "Mock burn rate verdict.",
                "estimated_roi_multiplier": 1.2,
                "margin_leak_percentage": 15
            }
        }
        return CampaignResponse(**data)

def test_generate_campaign_endpoint():
    app.dependency_overrides[LLMService] = MockLLMService
    client = TestClient(app)
    try:
        response = client.post(
            "/campaign/generate", 
            json={
                "raw_brief": "Some brand brief info",
                "cynicism_level": "ruthless",
                "total_budget_usd": 1500000,
                "custom_allocations": {
                    "Digital": 1000000,
                    "HoReCa": 500000
                }
            }
        )
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["campaign_meta"]["brand_name"] == "Mock Brand"
        assert "Cynicism Level: ruthless" in json_data["cmo_verdict"]
        assert "b2b_pitches" in json_data
        assert json_data["b2b_pitches"][0]["partner_name"] == "Mock Partner"
    finally:
        app.dependency_overrides.clear()

def test_export_pdf_endpoint():
    client = TestClient(app)
    campaign_data = {
        "campaign_meta": {
            "brand_name": "PDF Export Brand",
            "target_audience_analysis": "Cynical profile",
            "total_budget_usd": 1500000
        },
        "channels": [
            {
                "channel_name": "Digital",
                "allocation_percentage": 100,
                "allocation_budget_usd": 1500000,
                "core_strategy": "Strategy",
                "activations": ["Act"],
                "kpis": ["Kpi"]
            }
        ],
        "cmo_verdict": "Verdict text.",
        "b2b_pitches": [
            {
                "partner_name": "Goodwine",
                "target_role": "Buyer",
                "pitch_text": "Goodwine pitch content."
            }
        ],
        "financial_stress_test": {
            "risk_score": 45,
            "burn_rate_verdict": "Verdict text.",
            "estimated_roi_multiplier": 1.5,
            "margin_leak_percentage": 18
        }
    }
    response = client.post("/campaign/export", json=campaign_data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]

def test_negotiate_campaign_endpoint():
    client = TestClient(app)
    payload = {
        "strategy_context": {"brand_name": "Volya"},
        "chat_history": [
            {"sender": "buyer", "text": "Too expensive."}
        ],
        "user_message": "But we have a 35% margin."
    }
    response = client.post("/campaign/negotiate", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert "buyer_response" in json_data
    assert "deal_probability" in json_data
    assert "criticism_point" in json_data
