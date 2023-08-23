import { generatePath } from 'react-router-dom'

export const routes = {
  overview: {
    path: '/ingredients',
    build() {
      return generatePath(this.path)
    },
  },
}
