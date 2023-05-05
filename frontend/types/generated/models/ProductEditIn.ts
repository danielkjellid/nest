/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type ProductEditIn = {
    name: string;
    grossPrice: string;
    unitQuantity: string;
    unit: string;
    supplier: string;
    gtin?: string;
    odaId?: string;
    odaUrl?: string;
    isAvailable: boolean;
    isSynced: boolean;
    thumbnail?: Blob;
};

