/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UserRecord } from './UserRecord';

export type UserRecordListAPIResponse = {
    status: UserRecordListAPIResponse.status;
    message?: string;
    data?: Array<UserRecord>;
};

export namespace UserRecordListAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

