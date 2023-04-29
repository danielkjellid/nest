/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UnitListOut } from './UnitListOut';

export type UnitListOutAPIResponse = {
    status: UnitListOutAPIResponse.status;
    message?: string;
    data?: Array<UnitListOut>;
};

export namespace UnitListOutAPIResponse {

    export enum status {
        SUCCESS = 'success',
        ERROR = 'error',
    }


}

