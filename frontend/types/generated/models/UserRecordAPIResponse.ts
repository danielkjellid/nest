/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UserRecord } from './UserRecord';

export type UserRecordAPIResponse = {
    status: UserRecordAPIResponse.status;
    message?: string;
    data?: Array<UserRecord>;
};

export namespace UserRecordAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

