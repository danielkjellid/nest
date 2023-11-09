/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { IngredientListOut } from './IngredientListOut';

export type IngredientListOutAPIResponse = {
    status: IngredientListOutAPIResponse.status;
    message?: string;
    data?: Array<IngredientListOut>;
};

export namespace IngredientListOutAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

