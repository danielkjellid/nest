/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeCreateOut } from './RecipeCreateOut';

export type RecipeCreateOutAPIResponse = {
    status: RecipeCreateOutAPIResponse.status;
    message?: string;
    data?: RecipeCreateOut;
};

export namespace RecipeCreateOutAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

