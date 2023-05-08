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
    isAvailable: boolean;
    isSynced: boolean;
    thumbnail?: Blob;
};

