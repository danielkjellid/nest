/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductListOut } from './ProductListOut';

export type ProductListOutAPIResponse = {
    status: ProductListOutAPIResponse.status;
    message?: string;
    data?: Array<ProductListOut>;
};

export namespace ProductListOutAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

