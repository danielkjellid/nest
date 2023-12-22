/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RecipeCreateOut } from './RecipeCreateOut';

export type APIResponse_RecipeCreateOut_ = {
    status: APIResponse_RecipeCreateOut_.status;
    message?: (string | null);
    data: (RecipeCreateOut | null);
};

export namespace APIResponse_RecipeCreateOut_ {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

