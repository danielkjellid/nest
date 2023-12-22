/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type ProductCreateForm = {
    name: string;
    grossPrice: string;
    unitQuantity: string;
    unitId: number;
    supplier: string;
    gtin?: (string | null);
    ingredients?: (string | null);
    allergens?: (string | null);
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
    thumbnail?: (Blob | null);
};

