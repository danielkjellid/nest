/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeRecord } from './RecipeRecord';

export type RecipeRecordAPIResponse = {
    status: RecipeRecordAPIResponse.status;
    message?: string;
    data?: Array<RecipeRecord>;
};

export namespace RecipeRecordAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

