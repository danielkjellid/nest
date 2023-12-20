/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductRecord } from './ProductRecord';

export type ProductRecordListAPIResponse = {
    status: ProductRecordListAPIResponse.status;
    message?: string;
    data?: ProductRecord;
};

export namespace ProductRecordListAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

