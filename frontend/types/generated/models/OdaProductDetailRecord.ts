/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OdaProductAvailabilityRecord } from './OdaProductAvailabilityRecord';
import type { OdaProductBottleDepositRecord } from './OdaProductBottleDepositRecord';
import type { OdaProductCategoryDetailRecord } from './OdaProductCategoryDetailRecord';
import type { OdaProductClassifierRecord } from './OdaProductClassifierRecord';
import type { OdaProductDetailedInfo } from './OdaProductDetailedInfo';
import type { OdaProductDiscountRecord } from './OdaProductDiscountRecord';
import type { OdaProductImageRecord } from './OdaProductImageRecord';
import type { OdaProductMetadataRecord } from './OdaProductMetadataRecord';
import type { OdaProductPromotionRecord } from './OdaProductPromotionRecord';
import type { OdaProductRecord } from './OdaProductRecord';

export type OdaProductDetailRecord = {
    id: number;
    fullName: string;
    brand?: (string | null);
    brandId?: (number | null);
    name: string;
    nameExtra: string;
    frontUrl: string;
    absoluteUrl: string;
    grossPrice: string;
    grossUnitPrice: string;
    unitPriceQuantityAbbreviation: string;
    unitPriceQuantityName: string;
    clientClassifiers: Array<OdaProductClassifierRecord>;
    currency: any;
    discount?: (OdaProductDiscountRecord | null);
    /**
     * @deprecated
     */
    promotion?: (OdaProductPromotionRecord | null);
    promotions?: (Array<OdaProductPromotionRecord> | null);
    availability: OdaProductAvailabilityRecord;
    metadata: OdaProductMetadataRecord;
    images: Array<OdaProductImageRecord>;
    categories: Array<OdaProductCategoryDetailRecord>;
    contentsHtml: string;
    nutritionHtml: string;
    bottleDeposit?: (OdaProductBottleDepositRecord | null);
    alternativeProducts: Array<OdaProductRecord>;
    discountMixAndMatchProducts?: (Array<OdaProductRecord> | null);
    detailedInfo: OdaProductDetailedInfo;
    isProductIncludedInProductLists?: (boolean | null);
    isRestricted: boolean;
};

