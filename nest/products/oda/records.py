from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


##############
# Categories #
##############


class OdaProductCategoryCampaignBannerPromotionBubbleRecord(BaseModel):
    text: str
    color: str


class OdaProductCategoryCampaignBannerRecord(BaseModel):
    id: int
    image_url: str | None
    lead_text: str | None
    regular_text: str | None
    title: str | None
    description: str | None
    button_text: str | None
    link: str | None
    has_dark_overlay: bool
    promotion_bubble: OdaProductCategoryCampaignBannerPromotionBubbleRecord | None


class OdaProductCategoryRecord(BaseModel):
    id: int
    name: str
    uri: str | None


class OdaProductCategoryDetailRecord(BaseModel):
    id: int
    name: str
    slug: str
    parent: int | None
    parents: list[OdaProductCategoryRecord]


############################
# Discounts and promotions #
############################


class OdaProductDiscountRecord(BaseModel):
    is_discounted: bool
    undiscounted_gross_price: str
    undiscounted_gross_unit_price: str
    description_short: str
    maximum_quantity: int | None
    remaining_quantity: Decimal | None
    absolute_url: str


class OdaProductPromotionRecord(BaseModel):
    title: str
    title_color: str
    background_color: str
    text_color: str
    description_short: str | None
    accessibility_text: str
    display_style: str


###################
# Bottle deposits #
###################


class OdaProductBottleDepositRecord(BaseModel):
    is_included_in_price: bool
    fee: str


###############
# Classifiers #
###############


class OdaProductClassifierRecord(BaseModel):
    """
    Classifiers are specific product attributes at Oda. Such as:
    - Dangerous good
    - Very tender
    - Very fresh
    - Is frozen
    - is organic
    - Vegan
    - Lactose free
    - Gluten free
    """

    name: str
    image_url: str | None
    is_important: bool
    description: str


##########
# Images #
##########


class OdaProductImageInnerRecord(BaseModel):
    url: str
    width: int
    height: int


class OdaProductImageRecord(BaseModel):
    large: OdaProductImageInnerRecord
    thumbnail: OdaProductImageInnerRecord


###########
# Hazards #
###########


class OdaProductHazardSymbolRecord(BaseModel):
    code: str
    description: str
    image_url: str


class OdaProductHazardStatementRecord(BaseModel):
    code: str
    description: str


class OdaProductHazardSafetyDataSheetRecord(BaseModel):
    url: str
    title: str
    link_text: str


class OdaProductHazardRecord(BaseModel):
    title: str
    signal_word: str | None
    symbols: list[OdaProductHazardSymbolRecord] | None
    hazard_statements: list[OdaProductHazardStatementRecord] | None
    precautionary_statements: list[OdaProductHazardStatementRecord] | None
    safety_data_sheet: OdaProductHazardSafetyDataSheetRecord | None


##############
# Local info #
##############


class OdaProductLocalInfoBadgeRecord(BaseModel):
    badge_class: Literal["sodium-warning", "keep-frozen", "keep-cool", "pharmaceutical"]
    text: str
    label: str


class OdaProductLocalInfoKeywordEmphasisRecord(BaseModel):
    keywords: list[str]
    emphasis_type: Literal["bold", "normal"]
    reason: str | None


class OdaProductLocalInfoTableRow(BaseModel):
    key: str
    value: str
    badge: OdaProductLocalInfoBadgeRecord | None
    indent: int | None
    tooltip: str | None
    link: str | None
    emphasis: OdaProductLocalInfoKeywordEmphasisRecord | None
    key_id: str | None


class OdaProductLocalInfoTable(BaseModel):
    title: str | None
    rows: list[OdaProductLocalInfoTableRow]
    disclaimers: list[str] | None


class OdaProductLocalInfo(BaseModel):
    language: str
    language_name: str
    local_product_name: str
    short_description: str
    description_from_supplier: str | None
    nutrition_info_table: OdaProductLocalInfoTable
    contents_table: OdaProductLocalInfoTable
    hazards: OdaProductHazardRecord | None


class OdaProductDetailedInfo(BaseModel):
    country: Literal["NO"]  # We only want info from the norwegian market.
    local: list[OdaProductLocalInfo]


############
# Products #
############


class OdaProductAvailabilityRecord(BaseModel):
    is_available: bool
    description: str
    description_short: str
    code: Literal[
        "available",
        "available_later",
        "not_for_sale",
        "restricted_item_user_policy",
        "sold_out",
        "sold_out_partial",
        "sold_out_supplier",
        "unavailable_alcohol_time",
        "unavailable_temporarily",
        "unavailable_unattended",
        "unavailable_weekday",
        "unknown",
    ]


class OdaProductMetadataRecord(BaseModel):
    is_sponsor_labeled: bool | None = False


class OdaProductRecord(BaseModel):
    id: int
    full_name: str
    brand: str | None
    brand_id: int | None
    name: str
    name_extra: str
    front_url: str
    absolute_url: str
    gross_price: str
    gross_unit_price: str
    unit_price_quantity_abbreviation: str
    unit_price_quantity_name: str
    client_classifiers: list[OdaProductClassifierRecord]
    currency: Literal["NOK"]  # We only accept products from the norwegian market.
    discount: OdaProductDiscountRecord | None
    promotion: OdaProductPromotionRecord | None = Field(deprecated=True)
    promotions: list[OdaProductPromotionRecord] | None
    availability: OdaProductAvailabilityRecord
    metadata: OdaProductMetadataRecord
    images: list[OdaProductImageRecord]


class OdaProductDetailRecord(OdaProductRecord):
    categories: list[OdaProductCategoryDetailRecord]
    bottle_deposit: OdaProductBottleDepositRecord | None
    alternative_products: list[OdaProductRecord]
    discount_mix_and_match_products: list[OdaProductRecord] | None
    detailed_info: OdaProductDetailedInfo
    is_product_included_in_product_lists: bool | None
    is_restricted: bool
