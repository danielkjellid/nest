/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type OdaProductPromotionRecord = {
    title: string;
    titleColor: string;
    backgroundColor: string;
    textColor: string;
    descriptionShort?: string;
    accessibilityText: string;
    displayStyle: OdaProductPromotionRecord.displayStyle;
};

export namespace OdaProductPromotionRecord {

    export enum displayStyle {
        MIX_AND_MATCH = 'mix_and_match',
        MAX_ITEMS = 'max_items',
        FEW_LEFT = 'few_left',
        REGULAR_DISCOUNT = 'regular_discount',
        IS_NEW = 'is_new',
        RECOMMENDED = 'recommended',
        IN_SEASON = 'in_season',
        BESTSELLER = 'bestseller',
        CAMPAIGN_PRICE = 'campaign_price',
        WHOLESALE = 'wholesale',
        BEST_IN_TEST = 'best_in_test',
        TEST_WINNER = 'test_winner',
    }


}

