/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OdaProductDetailRecord } from './OdaProductDetailRecord';

export type OdaProductDetailRecordAPIResponse = {
    status: OdaProductDetailRecordAPIResponse.status;
    message?: string;
    data?: OdaProductDetailRecord;
};

export namespace OdaProductDetailRecordAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

