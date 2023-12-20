/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OdaProductHazardSafetyDataSheetRecord } from './OdaProductHazardSafetyDataSheetRecord';
import type { OdaProductHazardStatementRecord } from './OdaProductHazardStatementRecord';
import type { OdaProductHazardSymbolRecord } from './OdaProductHazardSymbolRecord';

export type OdaProductHazardRecord = {
    title: string;
    signalWord?: string;
    symbols?: Array<OdaProductHazardSymbolRecord>;
    hazardStatements?: Array<OdaProductHazardStatementRecord>;
    precautionaryStatements?: Array<OdaProductHazardStatementRecord>;
    safetyDataSheet?: OdaProductHazardSafetyDataSheetRecord;
};

