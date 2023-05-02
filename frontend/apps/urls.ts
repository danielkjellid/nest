const urls = {
  products: {
    detail: ({ id }: { id: number }) => `/api/v1/products/${id}/`,
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
