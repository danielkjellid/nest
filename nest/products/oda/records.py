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
    image_url: str | None = None
    lead_text: str | None = None
    regular_text: str | None = None
    title: str | None = None
    description: str | None = None
    button_text: str | None = None
    link: str | None = None
    has_dark_overlay: bool
    promotion_bubble: OdaProductCategoryCampaignBannerPromotionBubbleRecord | None = None


class OdaProductCategoryRecord(BaseModel):
    id: int
    name: str
    uri: str | None = None
    slug: str
    parent: int | None = None


class OdaProductCategoryDetailRecord(BaseModel):
    id: int
    name: str
    parent: int | None = None
    ordering: int
    description: str
    is_new: bool
    children: list["OdaProductCategoryDetailRecord"]
    parents: list[OdaProductCategoryRecord]
    siblings: list[OdaProductCategoryRecord]
    campaign_banners: list[OdaProductCategoryCampaignBannerRecord]


############################
# Discounts and promotions #
############################


class OdaProductDiscountRecord(BaseModel):
    is_discounted: bool
    undiscounted_gross_price: str
    undiscounted_gross_unit_price: str
    description_short: str
    maximum_quantity: int | None = None
    remaining_quantity: Decimal | None = None
    absolute_url: str


class OdaProductPromotionRecord(BaseModel):
    title: str
    title_color: str
    background_color: str
    text_color: str
    description_short: str | None = None
    accessibility_text: str
    display_style: Literal[
        "mix_and_match",
        "max_items",
        "few_left",
        "regular_discount",
        "is_new",
        "recommended",
        "in_season",
        "bestseller",
        "campaign_price",
        "wholesale",
        "best_in_test",
        "test_winner",
    ]


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
    image_url: str | None = None
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
    signal_word: str | None = None
    symbols: list[OdaProductHazardSymbolRecord] | None = None
    hazard_statements: list[OdaProductHazardStatementRecord] | None = None
    precautionary_statements: list[OdaProductHazardStatementRecord] | None = None
    safety_data_sheet: OdaProductHazardSafetyDataSheetRecord | None = None


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
    reason: str | None = None


class OdaProductLocalInfoTableRow(BaseModel):
    key: str
    value: str
    badge: OdaProductLocalInfoBadgeRecord | None = None
    indent: int | None = None
    tooltip: str | None = None
    link: str | None = None
    emphasis: OdaProductLocalInfoKeywordEmphasisRecord | None = None
    key_id: str | None = None


class OdaProductLocalInfoTable(BaseModel):
    title: str | None = None
    rows: list[OdaProductLocalInfoTableRow]
    disclaimers: list[str] | None = None


class OdaProductLocalInfo(BaseModel):
    language: str
    language_name: str
    local_product_name: str
    short_description: str
    description_from_supplier: str | None = None
    nutrition_info_table: OdaProductLocalInfoTable
    contents_table: OdaProductLocalInfoTable
    hazards: OdaProductHazardRecord | None = None


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
    brand: str | None = None
    brand_id: int | None = None
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
    discount: OdaProductDiscountRecord | None = None
    promotion: OdaProductPromotionRecord | None = Field(None, deprecated=True)
    promotions: list[OdaProductPromotionRecord] | None = None
    availability: OdaProductAvailabilityRecord
    metadata: OdaProductMetadataRecord
    images: list[OdaProductImageRecord]


class OdaProductDetailRecord(OdaProductRecord):
    categories: list[OdaProductCategoryDetailRecord]
    contents_html: str
    nutrition_html: str
    bottle_deposit: OdaProductBottleDepositRecord | None = None
    alternative_products: list[OdaProductRecord]
    discount_mix_and_match_products: list[OdaProductRecord] | None = None
    detailed_info: OdaProductDetailedInfo
    is_product_included_in_product_lists: bool | None = None
    is_restricted: bool
