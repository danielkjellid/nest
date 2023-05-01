/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UserListHomeOut } from './UserListHomeOut';

export type UserListOut = {
    id: number;
    email: string;
    fullName: string;
    isActive: boolean;
    isStaff: boolean;
    isSuperuser: boolean;
    home?: UserListHomeOut;
};
