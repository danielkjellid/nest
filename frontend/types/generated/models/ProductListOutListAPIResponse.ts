/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductListOut } from './ProductListOut';

export type ProductListOutListAPIResponse = {
    status: ProductListOutListAPIResponse.status;
    message?: string;
    data?: Array<ProductListOut>;
};

export namespace ProductListOutListAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

