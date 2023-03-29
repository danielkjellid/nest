import { IconHome, IconNews, IconSettings, IconShoppingCart, IconUsers } from '@tabler/icons-react'

import React from 'react'

const end = true

export default [
  { key: 'plans', path: '/', element: () => import('./plans'), icon: <IconHome />, end },
  {
    key: 'products',
    path: '/products/',
    element: () => import('./products'),
    icon: <IconShoppingCart />,
    end,
  },
  {
    key: 'recipes',
    path: '/recipes/',
    element: () => import('./recipes'),
    icon: <IconNews />,
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