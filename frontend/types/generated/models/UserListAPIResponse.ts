/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User } from './User';

export type UserListAPIResponse = {
    status: UserListAPIResponse.status;
    message?: string;
    data?: Array<User>;
};

export namespace UserListAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

