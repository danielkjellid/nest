/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { UnitType } from './UnitType';

export type UnitRecord = {
    id: number;
    name: string;
    namePluralized?: string;
    abbreviation: string;
    unitType: UnitType;
    baseFactor: number;
    isBaseUnit: boolean;
    isDefault: boolean;
    displayName: string;
};

