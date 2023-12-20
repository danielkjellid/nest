/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeIngredientRecord } from './RecipeIngredientRecord';

export type RecipeIngredientRecordAPIResponse = {
    status: RecipeIngredientRecordAPIResponse.status;
    message?: string;
    data?: Array<RecipeIngredientRecord>;
};

export namespace RecipeIngredientRecordAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

