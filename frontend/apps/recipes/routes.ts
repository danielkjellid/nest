import { generatePath } from 'react-router-dom'

export const routes = {
  overview: {
    path: '/recipes',
    build() {
      return generatePath(this.path)
    },
  },
  createRecipe: {
    path: '/recipes/create',
    build() {
      return generatePath(this.path)
    },
  },
  createRecipe2: {
    path: '/recipes/create2',
    build() {
      return generatePath(this.path)
    },
  },
  createRecipeIngredients: {
    path: '/recipes/create/:recipeId/ingredients',
    build({ recipeId }: { recipeId: string | number }) {
      return generatePath(this.path, { recipeId })
    },
  },
  createRecipeSteps: {
    path: '/recipes/create/:recipeId/steps',
    build({ recipeId }: { recipeId: string | number }) {
      return generatePath(this.path, { recipeId })
    },
  },
}
