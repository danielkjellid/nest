type Param = string | number

const urls = {
  ingredients: {
    list: () => '/api/v1/ingredients/',
    create: () => '/api/v1/ingredients/create/',
  },
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
    create: () => '/api/v1/recipes/create/',
    createSteps: ({ id }: { id: Param }) => `/api/v1/recipes/${id}/steps/create/`,
    listIngredientGroups: ({ id }: { id: Param }) => `/api/v1/recipes/${id}/ingredient-groups/`,
    createIngredientGroups: ({ id }: { id: Param }) =>
      `/api/v1/recipes/${id}/ingredient-groups/create/`,
  },
  users: {
    list: () => '/api/v1/users/',
  },
  units: {
    list: () => '/api/v1/units/',
  },
}

export { urls }
