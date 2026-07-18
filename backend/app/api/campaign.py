from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import io
from app.schemas.campaign import CampaignRequest, CampaignResponse, NegotiationRequest, NegotiationResponse
from app.services.llm import LLMService
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

router = APIRouter(prefix="/campaign", tags=["Campaign"])

@router.post("/generate", response_model=CampaignResponse)
async def generate_campaign(
    payload: CampaignRequest, 
    llm_service: LLMService = Depends()
):
    try:
        # Invoke the official OpenAI Structured Outputs parser, passing the full request payload
        strategy = await llm_service.generate_structured_strategy(payload)
        return strategy
    except Exception as e:
        # If OpenAI fails or key is missing, don't crash the server, return a clean 500 error
        raise HTTPException(
            status_code=500, 
            detail=f"OpenAI Generation failed: {str(e)}"
        )

@router.post("/export")
async def export_pdf(campaign: CampaignResponse):
    """
    Accepts the compiled CampaignResponse and returns a professional, downloadable 
    executive campaign brief in PDF format in-memory using reportlab, using USD currency.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=40, 
        leftMargin=40, 
        topMargin=40, 
        bottomMargin=40
    )
    story = []
    
    styles = getSampleStyleSheet()
    
    # Custom style colors
    primary_color = colors.HexColor("#06b6d4")  # Cyan 500
    text_color = colors.HexColor("#1e293b")  # Slate 800
    
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontSize=22,
        leading=26,
        textColor=primary_color,
        spaceAfter=15
    )
    
    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4f46e5"),  # Indigo 600
        spaceBefore=14,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        textColor=text_color,
        spaceAfter=8
    )
    
    bullet_style = ParagraphStyle(
        "BulletCustom",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=12,
        textColor=text_color,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    # Document contents assembly
    story.append(Paragraph("BriefToLaunch: Executive Campaign Brief", title_style))
    story.append(Paragraph(f"<b>Brand Name:</b> {campaign.campaign_meta.brand_name}", body_style))
    story.append(Paragraph(f"<b>Total Budget:</b> ${campaign.campaign_meta.total_budget_usd:,}", body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Target Audience Cynical Profile", section_style))
    story.append(Paragraph(campaign.campaign_meta.target_audience_analysis, body_style))
    
    story.append(Paragraph("Channel Budget Allocation & Core Strategy", section_style))
    for ch in campaign.channels:
        story.append(Paragraph(f"<b>{ch.channel_name} ({ch.allocation_percentage}% - ${ch.allocation_budget_usd:,})</b>", body_style))
        story.append(Paragraph(f"Strategy: {ch.core_strategy}", body_style))
        
        story.append(Paragraph("Activations:", body_style))
        for act in ch.activations:
            story.append(Paragraph(f"&bull; {act}", bullet_style))
            
        story.append(Paragraph("KPIs:", body_style))
        for kpi in ch.kpis:
            story.append(Paragraph(f"&bull; {kpi}", bullet_style))
        story.append(Spacer(1, 8))
        
    story.append(Paragraph("B2B Stakeholder Commercial Proposals", section_style))
    for pitch in campaign.b2b_pitches:
        story.append(Paragraph(f"<b>Partner: {pitch.partner_name} (Target: {pitch.target_role})</b>", body_style))
        story.append(Paragraph(pitch.pitch_text, body_style))
        story.append(Spacer(1, 6))
        
    story.append(Paragraph("Financial Stress Test & Capital Risk Index", section_style))
    story.append(Paragraph(f"<b>Risk Score:</b> {campaign.financial_stress_test.risk_score}/100", body_style))
    story.append(Paragraph(f"<b>Margin Leakage Risk:</b> {campaign.financial_stress_test.margin_leak_percentage}%", body_style))
    story.append(Paragraph(f"<b>Burn Rate Verdict:</b> {campaign.financial_stress_test.burn_rate_verdict}", body_style))
    story.append(Paragraph(f"<b>Estimated ROI Multiplier:</b> {campaign.financial_stress_test.estimated_roi_multiplier}x", body_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("CMO Strategy Verdict", section_style))
    story.append(Paragraph(f"<i>&ldquo;{campaign.cmo_verdict}&rdquo;</i>", body_style))
    
    doc.build(story)
    buffer.seek(0)
    return StreamingResponse(
        buffer, 
        media_type="application/pdf", 
        headers={"Content-Disposition": "attachment; filename=executive_brief.pdf"}
    )

@router.post("/negotiate", response_model=NegotiationResponse)
async def negotiate_campaign(
    payload: NegotiationRequest, 
    llm_service: LLMService = Depends()
):
    """
    Simulates a live B2B budget negotiation with a toxic Category Buyer.
    Takes user counter-arguments, history, and brand profiles to generate replies, objections, and deal odds.
    """
    try:
        response = await llm_service.negotiate_strategy(payload)
        return response
    except Exception as e:
        # Return structured 500 error on compilation failure
        raise HTTPException(
            status_code=500, 
            detail=f"Negotiation compiler error: {str(e)}"
        )
