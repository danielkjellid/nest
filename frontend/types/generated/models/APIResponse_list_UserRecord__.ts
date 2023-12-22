/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UserRecord } from './UserRecord';

export type APIResponse_list_UserRecord__ = {
    status: APIResponse_list_UserRecord__.status;
    message?: (string | null);
    data: (Array<UserRecord> | null);
};

export namespace APIResponse_list_UserRecord__ {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

