/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type ProductEditForm = {
    name: string;
    grossPrice: (number | string);
    unitQuantity: (number | string);
    unitId: number;
    supplier: string;
    gtin?: (string | null);
    odaId?: (number | null);
    odaUrl?: (string | null);
    fat?: (string | null);
    fatSaturated?: (string | null);
    fatMonounsaturated?: (string | null);
    fatPolyunsaturated?: (string | null);
    carbohydrates?: (string | null);
    carbohydratesSugars?: (string | null);
    carbohydratesPolyols?: (string | null);
    carbohydratesStarch?: (string | null);
    fibres?: (string | null);
    salt?: (string | null);
    sodium?: (string | null);
    isAvailable: boolean;
    isSynced: boolean;
    thumbnail?: (Blob | null);
};

