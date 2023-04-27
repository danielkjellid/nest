const urls = {
  products: {
    list: () => '/api/v1/products/',
    productImport: () => '/api/v1/products/import/',
    productAdd: () => '/api/v1/products/add/',
  },
  users: {
    list: () => '/api/v1/users/',
  },
  units: {
    list: () => '/api/v1/units/',
  },
}

export { urls }
