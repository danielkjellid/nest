/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ProductEditIn } from './ProductEditIn';

export type ProductEditInAPIResponse = {
    status: ProductEditInAPIResponse.status;
    message?: string;
    data?: ProductEditIn;
};

export namespace ProductEditInAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

