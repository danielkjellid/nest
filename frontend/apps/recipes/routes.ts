import { generatePath } from 'react-router-dom'

export const routes = {
  overview: {
    path: '/recipes',
    build: function () {
      return generatePath(this.path)
    },
  },
  create: {
    path: '/recipes/create',
    build: function () {
      return generatePath(this.path)
    },
  },
  edit: {
    path: '/recipes/:recipeId/edit',
    build: function ({ recipeId }: { recipeId: string | number }) {
      return generatePath(this.path, { recipeId: recipeId })
    },
  },
}
