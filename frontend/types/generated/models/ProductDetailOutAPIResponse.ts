/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductDetailOut } from './ProductDetailOut';

export type ProductDetailOutAPIResponse = {
    status: ProductDetailOutAPIResponse.status;
    message?: string;
    data?: ProductDetailOut;
};

export namespace ProductDetailOutAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

