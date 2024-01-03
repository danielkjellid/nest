type Param = string | number

const urls = {
  products: {
    create: () => '/api/v1/products/create/',
    detail: ({ id }: { id: Param }) => `/api/v1/products/${id}/`,
    edit: ({ id }: { id: Param }) => `/api/v1/products/${id}/edit/`,
    list: () => '/api/v1/products/',
    oda: {
      import: () => '/api/v1/products/oda/import/',
      importConfirm: () => '/api/v1/products/oda/import/confirm/',
    },
  },
  recipes: {
    list: () => '/api/v1/recipes/',
    create: () => '/api/v1/recipes/create2/',
    detail: ({ id }: { id: Param }) => `/api/v1/recipes/recipe/${id}/`,

    ingredients: {
      list: () => '/api/v1/recipes/ingredients/',
      create: () => '/api/v1/recipes/ingredients/create/',
      delete: () => '/api/v1/recipes/ingredients/delete/',
      groups: {
        list: ({ id }: { id: Param }) => `/api/v1/recipes/ingredients/${id}/groups/`,
        create: ({ id }: { id: Param }) => `/api/v1/recipes/ingredients/${id}/groups/create/`,
      },
    },
    steps: {
      create: ({ id }: { id: Param }) => `/api/v1/recipes/steps/${id}/create/`,
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
