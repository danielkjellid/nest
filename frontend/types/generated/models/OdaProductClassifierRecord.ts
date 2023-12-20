/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Classifiers are specific product attributes at Oda. Such as:
 * - Dangerous good
 * - Very tender
 * - Very fresh
 * - Is frozen
 * - is organic
 * - Vegan
 * - Lactose free
 * - Gluten free
 */
export type OdaProductClassifierRecord = {
    name: string;
    imageUrl?: string;
    isImportant: boolean;
    description: string;
};

