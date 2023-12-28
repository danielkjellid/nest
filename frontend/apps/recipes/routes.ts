import { generatePath } from 'react-router-dom'

export const routes = {
  overview: {
    path: '/recipes',
    build: function () {
      return generatePath(this.path)
    },
  },
  createRecipe: {
    path: '/recipes/create',
    build: function () {
      return generatePath(this.path)
    },
  },
  createRecipe2: {
    path: '/recipes/create2',
    build: function () {
      return generatePath(this.path)
    },
  },
  createRecipeIngredients: {
    path: '/recipes/create/:recipeId/ingredients',
    build: function ({ recipeId }: { recipeId: string | number }) {
      return generatePath(this.path, { recipeId: recipeId })
    },
  },
  createRecipeSteps: {
    path: '/recipes/create/:recipeId/steps',
    build: function ({ recipeId }: { recipeId: string | number }) {
      return generatePath(this.path, { recipeId: recipeId })
    },
  },
}
