import { generatePath } from 'react-router-dom'

export const routes = {
  overview: {
    path: '/products',
    build: function () {
      return generatePath(this.path)
    },
  },
  detail: {
    path: '/products/:productId',
    build: function ({ productId }: { productId: string | number }) {
      return generatePath(this.path, { productId: productId })
    },
  },
  edit: {
    path: '/products/:productId/edit',
    build: function ({ productId }: { productId: string | number }) {
      return generatePath(this.path, { productId: productId })
    },
  },
}
