/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UserListHome } from './UserListHome';

export type UserList = {
    id: number;
    email: string;
    fullName: string;
    isActive: boolean;
    isStaff: boolean;
    isSuperuser: boolean;
    home?: UserListHome;
};

