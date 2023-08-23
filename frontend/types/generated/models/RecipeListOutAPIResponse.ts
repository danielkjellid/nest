/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeListOut } from './RecipeListOut';

export type RecipeListOutAPIResponse = {
    status: RecipeListOutAPIResponse.status;
    message?: string;
    data?: Array<RecipeListOut>;
};

export namespace RecipeListOutAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

