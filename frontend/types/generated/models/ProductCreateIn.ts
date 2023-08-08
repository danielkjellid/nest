/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type ProductCreateIn = {
    name: string;
    grossPrice: string;
    unitQuantity: string;
    unit: number;
    supplier: string;
    gtin?: string;
    ingredients?: string;
    allergens?: string;
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
    thumbnail?: Blob;
};

