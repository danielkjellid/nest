/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OdaProductAvailabilityRecord } from './OdaProductAvailabilityRecord';
import type { OdaProductClassifierRecord } from './OdaProductClassifierRecord';
import type { OdaProductDiscountRecord } from './OdaProductDiscountRecord';
import type { OdaProductImageRecord } from './OdaProductImageRecord';
import type { OdaProductMetadataRecord } from './OdaProductMetadataRecord';
import type { OdaProductPromotionRecord } from './OdaProductPromotionRecord';

export type OdaProductRecord = {
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
    currency: OdaProductRecord.currency;
    discount?: OdaProductDiscountRecord;
    /**
     * @deprecated
     */
    promotion?: OdaProductPromotionRecord;
    promotions?: Array<OdaProductPromotionRecord>;
    availability: OdaProductAvailabilityRecord;
    metadata: OdaProductMetadataRecord;
    images: Array<OdaProductImageRecord>;
};

export namespace OdaProductRecord {

    export enum currency {
        NOK = 'NOK',
    }


}

