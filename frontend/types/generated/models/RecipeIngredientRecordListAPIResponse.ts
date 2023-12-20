/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientRecord } from './RecipeIngredientRecord';

export type RecipeIngredientRecordListAPIResponse = {
    status: RecipeIngredientRecordListAPIResponse.status;
    message?: string;
    data?: Array<RecipeIngredientRecord>;
};

export namespace RecipeIngredientRecordListAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

