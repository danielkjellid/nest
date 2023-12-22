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
};

