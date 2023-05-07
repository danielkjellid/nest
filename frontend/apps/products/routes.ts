import { generatePath } from 'react-router-dom'

export const routes = {
  overview: {
    path: '/products',
    build() {
      return generatePath(this.path)
    },
  },
  detail: {
    path: '/products/:productId',
    build({ productId }: { productId: string | number }) {
      return generatePath(this.path, { productId })
    },
  },
}
