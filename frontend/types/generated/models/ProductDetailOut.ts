/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductDetailAuditLogsOut } from './ProductDetailAuditLogsOut';
import type { ProductDetailUnitOut } from './ProductDetailUnitOut';

export type ProductDetailOut = {
    id: number;
    name: string;
    fullName: string;
    grossPrice: string;
    grossUnitPrice?: string;
    unit: ProductDetailUnitOut;
    unitQuantity?: string;
    odaUrl?: string;
    odaId?: string;
    isAvailable: boolean;
    thumbnailUrl?: string;
    gtin?: string;
    supplier: string;
    isSynced: boolean;
    auditLogs: Array<ProductDetailAuditLogsOut>;
};

