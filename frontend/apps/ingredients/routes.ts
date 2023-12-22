import { generatePath } from 'react-router-dom'

export const routes = {
  overview: {
    path: '/ingredients',
    build: function () {
      return generatePath(this.path)
    },
  },
}
