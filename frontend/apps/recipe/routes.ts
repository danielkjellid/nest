import { generatePath } from 'react-router-dom'

export const routes = {
  detail: {
    path: '/recipe/:recipeId',
    build({ recipeId }: { recipeId: string | number }) {
      return generatePath(this.path, { recipeId })
    },
  },
}
