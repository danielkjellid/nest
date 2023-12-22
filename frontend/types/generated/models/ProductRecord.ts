/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { LogEntryRecord } from './LogEntryRecord';
import type { ProductClassifiersRecord } from './ProductClassifiersRecord';
import type { TableRecord } from './TableRecord';
import type { UnitRecord } from './UnitRecord';

export type ProductRecord = {
    id: number;
    name: string;
    fullName: string;
    grossPrice: (number | string);
    grossUnitPrice?: (number | string | null);
    unit: UnitRecord;
    unitQuantity?: (number | string | null);
    odaUrl?: (string | null);
    odaId?: (number | null);
    isAvailable: boolean;
    isSynced: boolean;
    lastSyncedAt?: (string | null);
    thumbnailUrl?: (string | null);
    gtin?: (string | null);
    supplier?: (string | null);
    displayPrice: string;
    isOdaProduct: boolean;
    lastDataUpdate?: (string | null);
    lastDataUpdateDisplay?: (string | null);
    ingredients?: (string | null);
    allergens?: (string | null);
    classifiers: ProductClassifiersRecord;
    energyKj?: (number | string | null);
    energyKcal?: (number | string | null);
    fat?: (number | string | null);
    fatSaturated?: (number | string | null);
    fatMonounsaturated?: (number | string | null);
    fatPolyunsaturated?: (number | string | null);
    carbohydrates?: (number | string | null);
    carbohydratesSugars?: (number | string | null);
    carbohydratesPolyols?: (number | string | null);
    carbohydratesStarch?: (number | string | null);
    fibres?: (number | string | null);
    protein?: (number | string | null);
    salt?: (number | string | null);
    sodium?: (number | string | null);
    nutritionTable: Array<TableRecord>;
    auditLogs: Array<LogEntryRecord>;
};

