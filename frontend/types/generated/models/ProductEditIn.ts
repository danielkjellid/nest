/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type ProductEditIn = {
    name: string;
    grossPrice: number;
    unitQuantity: number;
    unit: number;
    supplier: string;
    gtin?: string;
    odaId?: number;
    odaUrl?: string;
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
    isAvailable: boolean;
    isSynced: boolean;
    thumbnail?: Blob;
};

