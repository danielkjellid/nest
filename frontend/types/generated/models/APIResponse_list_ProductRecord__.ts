/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductRecord } from './ProductRecord';

export type APIResponse_list_ProductRecord__ = {
    status: APIResponse_list_ProductRecord__.status;
    message?: (string | null);
    data: (Array<ProductRecord> | null);
};

export namespace APIResponse_list_ProductRecord__ {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

