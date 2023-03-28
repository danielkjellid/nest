import { MenuProvider, useMenu } from '../MenuProvider'
import { describe, expect, it, test } from 'vitest'

import React from 'react'
import { menuItemTestUtil } from './utils'
import { renderHook } from '@testing-library/react'

const menuData = [
  menuItemTestUtil('users', 'Users', true),
  menuItemTestUtil('products', 'Products', true),
]

describe('MenuContext context', () => {
  it('should throw an error if used outside provider', () => {
    test.fails('fail test', () => {
      const { result } = renderHook(() => useMenu())
      expect(result.current).rejects.toBe(0)
    })
  })

  it('should respond gracefully when used inside provider', () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => {
      return <MenuProvider menu={menuData}>{children}</MenuProvider>
    }

    const { result } = renderHook(() => useMenu(), { wrapper })

    expect(result.current.menu).toStrictEqual([
      { key: 'users', title: 'Users', end: true },
      { key: 'products', title: 'Products', end: true },
    ])
  })
})
