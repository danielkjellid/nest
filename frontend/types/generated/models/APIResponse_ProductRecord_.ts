/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductRecord } from './ProductRecord';

export type APIResponse_ProductRecord_ = {
    status: APIResponse_ProductRecord_.status;
    message?: (string | null);
    data: (ProductRecord | null);
};

export namespace APIResponse_ProductRecord_ {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

