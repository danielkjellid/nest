/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipePlanItemRecord } from './RecipePlanItemRecord';

export type RecipePlanRecord = {
    id: number;
    title: string;
    description: string;
    slug: string;
    fromDate: string;
    items: Array<RecipePlanItemRecord>;
};

