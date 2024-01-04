/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type RecipeCreateForm = {
    title: string;
    searchKeywords?: string;
    defaultNumPortions: number;
    status: RecipeCreateForm.status;
    difficulty: RecipeCreateForm.difficulty;
    externalId?: string;
    externalUrl?: string;
    isVegetarian?: boolean;
    isPescatarian?: boolean;
};

export namespace RecipeCreateForm {

    export enum status {
        DRAFT = 'draft',
        HIDDEN = 'hidden',
        PUBLISHED = 'published',
    }

    export enum difficulty {
        EASY = 'easy',
        MEDIUM = 'medium',
        HARD = 'hard',
    }


}

