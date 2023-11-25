/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductOdaImportOut } from './ProductOdaImportOut';

export type ProductOdaImportOutAPIResponse = {
    status: ProductOdaImportOutAPIResponse.status;
    message?: string;
    data?: ProductOdaImportOut;
};

export namespace ProductOdaImportOutAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

