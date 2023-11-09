/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UserListOut } from './UserListOut';

export type UserListOutAPIResponse = {
    status: UserListOutAPIResponse.status;
    message?: string;
    data?: Array<UserListOut>;
};

export namespace UserListOutAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

