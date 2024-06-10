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
    brand?: string;
    brandId?: number;
    name: string;
    nameExtra: string;
    frontUrl: string;
    absoluteUrl: string;
    grossPrice: string;
    grossUnitPrice: string;
    unitPriceQuantityAbbreviation: string;
    unitPriceQuantityName: string;
    clientClassifiers: Array<OdaProductClassifierRecord>;
    currency: OdaProductDetailRecord.currency;
    discount?: OdaProductDiscountRecord;
    /**
     * @deprecated
     */
    promotion?: OdaProductPromotionRecord;
    promotions?: Array<OdaProductPromotionRecord>;
    availability: OdaProductAvailabilityRecord;
    metadata: OdaProductMetadataRecord;
    images: Array<OdaProductImageRecord>;
    categories: Array<OdaProductCategoryDetailRecord>;
    bottleDeposit?: OdaProductBottleDepositRecord;
    alternativeProducts: Array<OdaProductRecord>;
    discountMixAndMatchProducts?: Array<OdaProductRecord>;
    detailedInfo: OdaProductDetailedInfo;
    isProductIncludedInProductLists?: boolean;
    isRestricted: boolean;
};

export namespace OdaProductDetailRecord {

    export enum currency {
        NOK = 'NOK',
    }


}

