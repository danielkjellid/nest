import { generatePath } from 'react-router-dom'

export const routes = {
  overview: {
    path: '/recipes',
    build() {
      return generatePath(this.path)
    },
  },
  ingredientsOverview: {
    path: '/recipes/ingredients',
    build() {
      return generatePath(this.path)
    },
  },
}
