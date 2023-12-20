/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductClassifiersRecord } from './ProductClassifiersRecord';
import type { UnitRecord } from './UnitRecord';

export type ProductRecord = {
    id: number;
    name: string;
    fullName: string;
    grossPrice: number;
    grossUnitPrice?: number;
    unit: UnitRecord;
    unitQuantity?: number;
    odaUrl?: string;
    odaId?: number;
    isAvailable: boolean;
    isSynced: boolean;
    lastSyncedAt?: string;
    thumbnailUrl?: string;
    gtin?: string;
    supplier?: string;
    displayPrice: string;
    isOdaProduct: boolean;
    lastDataUpdate?: string;
    ingredients?: string;
    allergens?: string;
    classifiers: ProductClassifiersRecord;
    energyKj?: number;
    energyKcal?: number;
    fat?: number;
    fatSaturated?: number;
    fatMonounsaturated?: number;
    fatPolyunsaturated?: number;
    carbohydrates?: number;
    carbohydratesSugars?: number;
    carbohydratesPolyols?: number;
    carbohydratesStarch?: number;
    fibres?: number;
    protein?: number;
    salt?: number;
    sodium?: number;
};

