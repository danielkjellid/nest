import { generatePath } from 'react-router-dom'

export const routes = {
  detail: {
    path: '/recipe/:recipeId',
    build: function ({ recipeId }: { recipeId: string | number }) {
      return generatePath(this.path, { recipeId: recipeId })
    },
  },
}
