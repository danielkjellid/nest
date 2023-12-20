/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductRecord } from './ProductRecord';

export type ProductRecordAPIResponse = {
    status: ProductRecordAPIResponse.status;
    message?: string;
    data?: Array<ProductRecord>;
};

export namespace ProductRecordAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

