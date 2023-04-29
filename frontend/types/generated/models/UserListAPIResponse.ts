/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UserList } from './UserList';

export type UserListAPIResponse = {
    status: UserListAPIResponse.status;
    message?: string;
    data?: Array<UserList>;
};

export namespace UserListAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

