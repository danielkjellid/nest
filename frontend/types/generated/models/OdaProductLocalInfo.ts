/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OdaProductHazardRecord } from './OdaProductHazardRecord';
import type { OdaProductLocalInfoTable } from './OdaProductLocalInfoTable';

export type OdaProductLocalInfo = {
    language: string;
    languageName: string;
    localProductName: string;
    shortDescription: string;
    descriptionFromSupplier?: (string | null);
    nutritionInfoTable: OdaProductLocalInfoTable;
    contentsTable: OdaProductLocalInfoTable;
    hazards?: (OdaProductHazardRecord | null);
};

