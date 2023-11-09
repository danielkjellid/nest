/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductDetailAuditLogsOut } from './ProductDetailAuditLogsOut';
import type { ProductDetailUnitOut } from './ProductDetailUnitOut';
import type { TableRecord } from './TableRecord';

export type ProductDetailOut = {
    id: number;
    name: string;
    fullName: string;
    isAvailable: boolean;
    thumbnailUrl?: string;
    containsLactose?: boolean;
    containsGluten?: boolean;
    grossPrice: string;
    grossUnitPrice?: string;
    unit: ProductDetailUnitOut;
    unitQuantity?: string;
    gtin?: string;
    supplier?: string;
    isSynced: boolean;
    odaId?: string;
    odaUrl?: string;
    isOdaProduct: boolean;
    lastDataUpdate?: string;
    fat?: string;
    fatSaturated?: string;
    fatMonounsaturated?: string;
    fatPolyunsaturated?: string;
    carbohydrates?: string;
    carbohydratesSugars?: string;
    carbohydratesPolyols?: string;
    carbohydratesStarch?: string;
    fibres?: string;
    salt?: string;
    sodium?: string;
    nutritionTable: Array<TableRecord>;
    auditLogs: Array<ProductDetailAuditLogsOut>;
};

