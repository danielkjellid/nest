/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductDetailAuditLogsOut } from './ProductDetailAuditLogsOut';
import type { ProductDetailNutritionOut } from './ProductDetailNutritionOut';
import type { ProductDetailUnitOut } from './ProductDetailUnitOut';

export type ProductDetailOut = {
    id: number;
    name: string;
    fullName: string;
    isAvailable: boolean;
    thumbnailUrl?: string;
    containsLactose: boolean;
    containsGluten: boolean;
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
    nutrition: Array<ProductDetailNutritionOut>;
    auditLogs: Array<ProductDetailAuditLogsOut>;
};

