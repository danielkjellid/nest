/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipePlanRecord } from './RecipePlanRecord';

export type RecipePlanRecordListAPIResponse = {
    status: RecipePlanRecordListAPIResponse.status;
    message?: string;
    data?: Array<RecipePlanRecord>;
};

export namespace RecipePlanRecordListAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

