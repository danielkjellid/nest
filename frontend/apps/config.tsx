import {
  IconHome,
  IconListDetails,
  IconNews,
  IconSettings,
  IconShoppingCart,
  IconUsers,
} from '@tabler/icons-react'

const end = true

export default [
  { key: 'plans', path: '/', element: () => import('./plans'), icon: <IconHome />, end },
  {
    key: 'products',
    path: '/products/*',
    element: () => import('./products'),
    icon: <IconShoppingCart />,
  },
  {
    key: 'recipes',
    path: '/recipes/*',
    element: () => import('./recipes'),
    icon: <IconNews />,
    end,
  },
  {
    key: 'ingredients',
    path: '/ingredients/*',
    element: () => import('./ingredients'),
    icon: <IconListDetails />,
    end,
  },
  {
    key: 'settings',
    path: '/settings/',
    element: () => import('./settings'),
    icon: <IconSettings />,
    end,
  },
  {
    key: 'users',
    path: '/users/',
    element: () => import('./users'),
    icon: <IconUsers />,
    end,
  },
]
