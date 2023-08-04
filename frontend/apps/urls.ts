type Param = string | number

const urls = {
  products: {
    create: () => '/api/v1/products/create/',
    detail: ({ id }: { id: Param }) => `/api/v1/products/${id}/`,
    edit: ({ id }: { id: Param }) => `/api/v1/products/${id}/edit/`,
    editFetch: ({ id }: { id: Param }) => `/api/v1/products/${id}/edit/`,
    list: () => '/api/v1/products/',

    oda: {
      import: () => '/api/v1/products/oda/import/',
      importConfirm: () => '/api/v1/products/oda/import/confirm/',
    },

    nutrition: {
      detail: ({ id }: { id: Param }) => `/api/v1/products/${id}/nutrition/`,
      edit: ({ id }: { id: Param }) => `/api/v1/products/${id}/nutrition/edit/`,
    },
  },
  users: {
    list: () => '/api/v1/users/',
  },
  units: {
    list: () => '/api/v1/units/',
  },
}

export { urls }
