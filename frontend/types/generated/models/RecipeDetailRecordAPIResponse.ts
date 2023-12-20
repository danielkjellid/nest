/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeDetailRecord } from './RecipeDetailRecord';

export type RecipeDetailRecordAPIResponse = {
    status: RecipeDetailRecordAPIResponse.status;
    message?: string;
    data?: RecipeDetailRecord;
};

export namespace RecipeDetailRecordAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

