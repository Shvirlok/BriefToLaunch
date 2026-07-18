from openai import AsyncOpenAI
from app.core.config import settings
from app.schemas.campaign import (
    CampaignResponse, 
    CampaignRequest, 
    ChannelAllocation, 
    CampaignMeta, 
    B2BPitch, 
    FinancialStressTest,
    NegotiationRequest,
    NegotiationResponse
)
from app.prompts.cmo_prompt import CYNICAL_CMO_PROMPT

class LLMService:
    """
    LLM Service utilizing the official OpenAI SDK and native Structured Outputs
    to generate fully structured CampaignResponse objects.
    """
    def __init__(self):
        # AsyncOpenAI client automatically reads OPENAI_API_KEY from environment or settings
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    async def generate_structured_strategy(self, request: CampaignRequest) -> CampaignResponse:
        """
        Sends the campaign brief to GPT-4o with Structured Outputs response formatting,
        applying custom cynicism levels and budget overrides. If a placeholder/dummy API key is used,
        returns a fully formed and validated mock response.
        """
        cynicism_level = request.cynicism_level.lower()
        custom_allocations = request.custom_allocations
        raw_brief = request.raw_brief
        total_budget = request.total_budget_usd
        
        # Intercept call if dummy key is configured to prevent API failures in testing/evaluation
        api_key = settings.OPENAI_API_KEY.lower()
        if "placeholder" in api_key or "dummy" in api_key:
            # Build mock channels mapping custom overrides if provided, otherwise using default splits
            if custom_allocations:
                allocations = custom_allocations
            else:
                allocations = {
                    "HoReCa": int(total_budget * 0.40),
                    "Digital": int(total_budget * 0.20),
                    "Retail": int(total_budget * 0.25),
                    "CSR": int(total_budget * 0.15)
                }
                # Fix minor rounding errors to ensure strict sum limit matches total_budget
                alloc_sum = sum(allocations.values())
                if alloc_sum != total_budget:
                    allocations["HoReCa"] += (total_budget - alloc_sum)

            mock_channels = []
            for ch_name, budget in allocations.items():
                percentage = int(round((budget / total_budget) * 100))
                
                if ch_name == "HoReCa":
                    core_strat = "Physical bar placements in premium metropolitan hubs utilizing raw recycled components to attract design-conscious buyers."
                    acts = [
                        "Launch premium AeroVibe product testing stations at bar counters in Kiev's top 15 design-focused cocktail lounges.",
                        "Provide bartenders with branded AeroVibe recycled composite serving trays and premium gear bags.",
                        "Offer signature cocktails with high-margin returns to venue managers, themed around eco-minimalism."
                    ]
                    kpis = [
                        "Direct venue placements: 15 design lounges",
                        "Product hands-on interactions: 5,000 users within 30 days",
                        "Retail QR code scan conversions: 2.5% rate"
                    ]
                elif ch_name == "Digital":
                    core_strat = "Hyper-targeted geo-ads around business parks and co-working spaces driving direct conversions."
                    acts = [
                        "Deploy localized Instagram, LinkedIn, and Telegram geo-ads around Kyiv business centers.",
                        "Launch a high-converting green-verification gateway that calculates e-waste mitigation profiles.",
                        "Publish dynamic, cynically honest e-waste progress updates via micro-influencers."
                    ]
                    kpis = [
                        "Click-through rate (CTR) on business centers: >3.2%",
                        "Gateway user completions: 4,000 unique leads",
                        "Conversion to sales: 1.5% rate"
                    ]
                elif ch_name == "Retail":
                    core_strat = "Interactive endcap displays in flagship Apple Premium Resellers to capture eco-conscious shoppers."
                    acts = [
                        "Install custom raw recycled composite display endcaps in Goodwine and Apple Premium boutiques.",
                        "Host premium product launch events in-store with sustainable accessory giveaways.",
                        "Run silent tastings or hardware demos led by specialist sustainable tech consultants."
                    ]
                    kpis = [
                        "Boutique endcap placements: 6 flagship locations",
                        "Monthly store sales volume increase: +28%",
                        "Interactive display engagement rate: 4.5%"
                    ]
                else:  # CSR
                    core_strat = "Direct, auditable funding to regional e-waste recycling facilities to build real solar-powered hubs."
                    acts = [
                        "Finance construction of 2 regional solar-powered e-waste collection hubs with verified solar rigs.",
                        "Deploy 10 modern composite recycling booths in prime urban neighborhoods.",
                        "Publish a real-time, public budget-expenditure ledger showing serial numbers and solar receipts."
                    ]
                    kpis = [
                        "Solar hubs fully operational before winter: 2 facilities",
                        "Urban composite e-waste booths deployed: 10 booths",
                        "E-waste collected: 15 metric tons in year 1"
                    ]
                
                mock_channels.append(
                    ChannelAllocation(
                        channel_name=ch_name,
                        allocation_percentage=percentage,
                        allocation_budget_usd=budget,
                        core_strategy=core_strat,
                        activations=acts,
                        kpis=kpis
                    )
                )

            verdict_prefix = ""
            if cynicism_level == "realistic":
                verdict_prefix = "[REALISTIC MODE] The numbers align and present a viable strategy. "
            elif cynicism_level == "hardcore":
                verdict_prefix = "[HARDCORE MODE] A biting, necessary response to boring marketing. "
            elif cynicism_level == "ruthless":
                verdict_prefix = "[RUTHLESS MODE] Zero-fluff execution that cuts out wasted advertising capital. "

            # Build mock B2BPitch list for AeroVibe dynamic partners
            mock_pitches = [
                B2BPitch(
                    partner_name="Apple Resellers",
                    target_role="Accessories Category Buyer",
                    pitch_text=(
                        f"AeroVibe delivers a premium accessory suite yielding a 42% gross margin. Backed by custom raw recycled "
                        f"composite display panels on-shelf, we appeal directly to affluent tech professionals looking for authentic "
                        f"eco-friendly design, driving high category basket values without relying on cheap discount tags."
                    )
                ),
                B2BPitch(
                    partner_name="SolarHub NGOs",
                    target_role="Chief Sustainability Officer",
                    pitch_text=(
                        f"Direct operational partnership framework directing exactly ${int(total_budget * 0.15):,} (15% of total budget) "
                        f"straight to the solar-powered recycling hub constructions. Bypasses standard administrative overheads "
                        f"and guarantees solar rig capacity metrics, providing a no-nonsense campaign devoid of empty PR greenwashing."
                    )
                ),
                B2BPitch(
                    partner_name="Design Lounges",
                    target_role="General Manager & GM Owner",
                    pitch_text=(
                        f"Exclusive spirits menu partnership integration. We supply composite serving trays, LED-lighted accessory "
                        f"stands, and custom menu listings yielding high margin returns. Leverages affluent urban tech professionals "
                        f"looking for local premium brands, increasing your average order profit margin by 18%."
                    )
                )
            ]

            # Build mock stress test
            mock_stress = FinancialStressTest(
                risk_score=78 if cynicism_level == "ruthless" else (65 if cynicism_level == "hardcore" else 48),
                burn_rate_verdict=(
                    f"Capital burn index is highly elevated due to front-loaded POS display physical overhead. "
                    f"Retail setups will bleed cash in the first 30 days. High probability of wasted retail capital "
                    f"unless Reseller conversions meet the projected targets."
                ),
                estimated_roi_multiplier=1.85 if cynicism_level == "realistic" else 1.45,
                margin_leak_percentage=16 if cynicism_level == "ruthless" else (22 if cynicism_level == "hardcore" else 28)
            )

            return CampaignResponse(
                campaign_meta=CampaignMeta(
                    brand_name="AeroVibe Premium Electronics",
                    target_audience_analysis=(
                        "Affluent tech professionals in metropolitan hubs who value eco-friendly status symbols "
                        "and premium industrial design but are highly immune to cheap corporate greenwashing slogans."
                    ),
                    total_budget_usd=total_budget
                ),
                channels=mock_channels,
                cmo_verdict=(
                    f"{verdict_prefix}This strategy works because it avoids typical pathetic environment tropes that urban tech professionals mock. "
                    "By positioning e-waste recycling as clean industrial design and executing direct auditable CSR solar hubs, "
                    "we cut through the marketing fluff. Keep the tone dry, pay the reseller partners on time, and make sure the composite panels don't look cheap."
                ),
                b2b_pitches=mock_pitches,
                financial_stress_test=mock_stress
            )
        
        # Build system prompt dynamic cynicism adjustments
        system_prompt = CYNICAL_CMO_PROMPT
        if cynicism_level == "realistic":
            system_prompt += "\n\nYour cynicism level is REALISTIC. Deliver a direct, highly grounded, and professional critique of standard marketing assumptions."
        elif cynicism_level == "hardcore":
            system_prompt += "\n\nYour cynicism level is HARDCORE. Be biting, sharp, highly skeptical, and dissect every promotional claim with a critical lens."
        elif cynicism_level == "ruthless":
            system_prompt += "\n\nYour cynicism level is RUTHLESS. Be extremely blunt, brutally honest, and cut through all corporate fluff. Explicitly point out wasted capital, redundant initiatives, and useless marketing buzzwords."

        # Add instructions for dynamic B2B Pitches extraction & Financial Stress Test
        system_prompt += (
            "\n\nCRITICAL SAAS REQUIREMENTS:\n"
            "1. Do not use pre-defined companies. Dynamically extract the primary commercial partners, "
            "retail networks, venue groups, or charity entities directly from the user's input brief.\n"
            "2. For each extracted entity, generate a highly optimized, cold, margin-driven commercial B2B pitch inside the `b2b_pitches` array, "
            "populating the fields: 'partner_name', 'target_role', and 'pitch_text'.\n"
            "3. Perform a cynical financial stress test based on current budget allocations. Calculate the 'risk_score' (int from 0 to 100), "
            "write a sharp 'burn_rate_verdict' explaining capital burn threats, and estimate a realistic 'estimated_roi_multiplier' (float, e.g. 1.25).\n"
            "4. Calculate the 'margin_leak_percentage' (int from 0 to 100) representing the exact percentage of the budget likely wasted on hidden agency commissions, "
            "inefficient B2B discounts, or logistical friction under the current split."
        )

        # Build user message with custom allocations constraint
        user_message = f"Here is the raw brand brief:\n\n{raw_brief}"
        if custom_allocations:
            allocations_str = ", ".join([f"'{channel}': {budget} USD" for channel, budget in custom_allocations.items()])
            user_message += (
                f"\n\nCRITICAL: The user has manually overridden the financial split. "
                f"You MUST strictly use these exact numbers for the channel allocations: {{{allocations_str}}}. "
                f"Re-align all strategic actions, scopes, and target KPIs to mathematically perfectly fit these specific numbers."
            )

        completion = await self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format=CampaignResponse
        )
        
        parsed_response = completion.choices[0].message.parsed
        if parsed_response is None:
            raise ValueError("OpenAI failed to parse the response into the CampaignResponse schema.")
            
        return parsed_response

    async def negotiate_strategy(self, request: NegotiationRequest) -> NegotiationResponse:
        """
        Simulates an interactive B2B negotiation with a toxic category buyer category retail gatekeeper.
        Tears apart user claims and budget overrides. Supports a local fallback if dummy keys are set.
        """
        user_msg = request.user_message.lower()
        strategy_context = request.strategy_context
        chat_history = request.chat_history
        
        # Intercept call if dummy key is configured
        api_key = settings.OPENAI_API_KEY.lower()
        if "placeholder" in api_key or "dummy" in api_key:
            deal_prob = 35
            objection = "High capital burn rate on physical fixtures."
            response_text = (
                "Your budget allocations are completely disproportionate. Why are you spending so much on "
                "composite panels? That is capital that does not drive conversion. We care about shelf margins. "
                "Unless you reduce the marketing overhead and guarantee a higher category rebate tier, we cannot list you."
            )
            
            if "margin" in user_msg or "profit" in user_msg or "35%" in user_msg or "72%" in user_msg or "42%" in user_msg:
                deal_prob = 65
                objection = "Volume velocity guarantees."
                response_text = (
                    "Okay, a 42% margin is a starting point, but what guarantees do we have on volume velocity? "
                    "Premium boutique shelf space is expensive. How does your CSR solar hub campaign "
                    "physically push sales off-take? Convince me that recycled component panels will shift inventory."
                )
            elif "donation" in user_msg or "recycle" in user_msg or "hub" in user_msg or "csr" in user_msg:
                deal_prob = 50
                objection = "CSR ROI leakage."
                response_text = (
                    "The CSR component builds brand goodwill, but it doesn't solve the immediate category retail risk. "
                    "Boutique buyers look for cold math. How will you target local geofenced audiences to convert "
                    "bystanders into hardware purchases in-store? Give me numbers, not CSR stories."
                )
            elif "retail" in user_msg or "boutique" in user_msg or "reseller" in user_msg:
                deal_prob = 58
                objection = "Display saturation and listing fee splits."
                response_text = (
                    "Listing in Apple Premium Resellers is ambitious. But boutiques are loyal to larger accessories brands. "
                    "What makes you think custom endcaps can offset the massive initial display counter installation costs? "
                    "I need to see a tighter amortization schedule."
                )

            return NegotiationResponse(
                buyer_response=response_text,
                deal_probability=deal_prob,
                criticism_point=objection
            )

        # Call OpenAI Structured Outputs
        system_prompt = (
            "You are a notoriously difficult, toxic, margin-obsessed corporate category buyer and retail gatekeeper. "
            "You are reviewing the user's proposed campaign strategy. You look for reasons to reject proposals, "
            "explicitly highlighting capital risks, wasted marketing budget, and demanding higher listing discounts. "
            "Critically analyze the user's messages and strategy context. Defend your shelf space. "
            "Return: buyer_response, deal_probability (integer 0-100), and criticism_point (brief key objection string)."
        )
        
        formatted_history = []
        for msg in chat_history:
            role = "assistant" if msg.sender == "buyer" else "user"
            formatted_history.append({"role": role, "content": msg.text})

        context_str = f"Strategy Data Context: {strategy_context}\nUser Counter-Argument: {request.user_message}"
        
        completion = await self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                *formatted_history,
                {"role": "user", "content": context_str}
            ],
            response_format=NegotiationResponse
        )
        
        parsed_response = completion.choices[0].message.parsed
        if parsed_response is None:
            raise ValueError("OpenAI failed to parse the response into the NegotiationResponse schema.")
            
        return parsed_response
export_pdf = None
