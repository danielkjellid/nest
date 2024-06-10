/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OdaProductCategoryRecord } from './OdaProductCategoryRecord';

export type OdaProductCategoryDetailRecord = {
    id: number;
    name: string;
    slug: string;
    parent?: number;
    parents: Array<OdaProductCategoryRecord>;
};

