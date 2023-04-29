/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductImportOut } from './ProductImportOut';

export type ProductImportOutAPIResponse = {
    status: ProductImportOutAPIResponse.status;
    message?: string;
    data?: ProductImportOut;
};

export namespace ProductImportOutAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

