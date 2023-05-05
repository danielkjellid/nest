import { generatePath } from 'react-router-dom'

export const routes = {
  overview: {
    path: '/products',
    build() {
      return generatePath(this.path)
    },
  },
}
