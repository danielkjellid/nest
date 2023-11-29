/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { HomeRecord } from './HomeRecord';

export type User = {
    id: number;
    email: string;
    firstName: string;
    lastName: string;
    fullName: string;
    isActive: boolean;
    isStaff: boolean;
    isSuperuser: boolean;
    isHijacked?: boolean;
    home?: HomeRecord;
};

