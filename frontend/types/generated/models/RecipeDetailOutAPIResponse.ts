/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeDetailOut } from './RecipeDetailOut';

export type RecipeDetailOutAPIResponse = {
    status: RecipeDetailOutAPIResponse.status;
    message?: string;
    data?: RecipeDetailOut;
};

export namespace RecipeDetailOutAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

