/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type OdaProductAvailabilityRecord = {
    isAvailable: boolean;
    description: string;
    descriptionShort: string;
    code: OdaProductAvailabilityRecord.code;
};

export namespace OdaProductAvailabilityRecord {

    export enum code {
        AVAILABLE = 'available',
        AVAILABLE_LATER = 'available_later',
        NOT_FOR_SALE = 'not_for_sale',
        RESTRICTED_ITEM_USER_POLICY = 'restricted_item_user_policy',
        SOLD_OUT = 'sold_out',
        SOLD_OUT_PARTIAL = 'sold_out_partial',
        SOLD_OUT_SUPPLIER = 'sold_out_supplier',
        UNAVAILABLE_ALCOHOL_TIME = 'unavailable_alcohol_time',
        UNAVAILABLE_TEMPORARILY = 'unavailable_temporarily',
        UNAVAILABLE_UNATTENDED = 'unavailable_unattended',
        UNAVAILABLE_WEEKDAY = 'unavailable_weekday',
        UNKNOWN = 'unknown',
    }


}

