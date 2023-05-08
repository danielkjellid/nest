type Param = string | number

const urls = {
  products: {
    detail: ({ id }: { id: Param }) => `/api/v1/products/${id}/`,
    edit: ({ id }: { id: Param }) => `/api/v1/products/${id}/edit/`,
    list: () => '/api/v1/products/',
    create: () => '/api/v1/products/create/',
  },
  users: {
    list: () => '/api/v1/users/',
  },
  units: {
    list: () => '/api/v1/units/',
  },
}

export { urls }
