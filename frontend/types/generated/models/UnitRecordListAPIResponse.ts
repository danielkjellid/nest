/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UnitRecord } from './UnitRecord';

export type UnitRecordListAPIResponse = {
    status: UnitRecordListAPIResponse.status;
    message?: string;
    data?: Array<UnitRecord>;
};

export namespace UnitRecordListAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

