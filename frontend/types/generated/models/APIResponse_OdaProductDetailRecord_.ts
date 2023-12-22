/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OdaProductDetailRecord } from './OdaProductDetailRecord';

export type APIResponse_OdaProductDetailRecord_ = {
    status: APIResponse_OdaProductDetailRecord_.status;
    message?: (string | null);
    data: (OdaProductDetailRecord | null);
};

export namespace APIResponse_OdaProductDetailRecord_ {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

