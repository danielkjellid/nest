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
}
