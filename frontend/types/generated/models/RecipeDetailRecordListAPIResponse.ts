/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeDetailRecord } from './RecipeDetailRecord';

export type RecipeDetailRecordListAPIResponse = {
    status: RecipeDetailRecordListAPIResponse.status;
    message?: string;
    data?: Array<RecipeDetailRecord>;
};

export namespace RecipeDetailRecordListAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

