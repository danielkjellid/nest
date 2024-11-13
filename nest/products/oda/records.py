from pydantic import BaseModel

##########
# Images #
##########


class OdaProductImageInnerRecord(BaseModel):
    url: str


class OdaProductImageRecord(BaseModel):
    thumbnail: OdaProductImageInnerRecord


##############
# Local info #
##############


class OdaProductLocalInfoKeywordEmphasisRecord(BaseModel):
    keywords: list[str]
    reason: str | None


class OdaProductLocalInfoTableRow(BaseModel):
    key: str
    value: str
    emphasis: OdaProductLocalInfoKeywordEmphasisRecord | None


class OdaProductLocalInfoTable(BaseModel):
    rows: list[OdaProductLocalInfoTableRow]


class OdaProductLocalInfo(BaseModel):
    nutrition_info_table: OdaProductLocalInfoTable
    contents_table: OdaProductLocalInfoTable


class OdaProductDetailedInfo(BaseModel):
    local: list[OdaProductLocalInfo]


############
# Products #
############


class OdaProductAvailabilityRecord(BaseModel):
    is_available: bool


class OdaProductRecord(BaseModel):
    id: int
    full_name: str
    front_url: str
    brand: str | None
    gross_price: str
    gross_unit_price: str
    unit_price_quantity_abbreviation: str
    availability: OdaProductAvailabilityRecord
    images: list[OdaProductImageRecord]


class OdaProductDetailRecord(OdaProductRecord):
    detailed_info: OdaProductDetailedInfo
