/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OdaProductAvailabilityRecord } from './OdaProductAvailabilityRecord';
import type { OdaProductDetailedInfo } from './OdaProductDetailedInfo';
import type { OdaProductImageRecord } from './OdaProductImageRecord';

export type OdaProductDetailRecord = {
    id: number;
    fullName: string;
    brand?: string;
    grossPrice: string;
    grossUnitPrice: string;
    unitPriceQuantityAbbreviation: string;
    availability: OdaProductAvailabilityRecord;
    images: Array<OdaProductImageRecord>;
    detailedInfo: OdaProductDetailedInfo;
};

