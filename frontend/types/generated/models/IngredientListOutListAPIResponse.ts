/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { IngredientListOut } from './IngredientListOut';

export type IngredientListOutListAPIResponse = {
    status: IngredientListOutListAPIResponse.status;
    message?: string;
    data?: Array<IngredientListOut>;
};

export namespace IngredientListOutListAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

