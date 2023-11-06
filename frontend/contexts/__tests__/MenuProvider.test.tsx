import { renderHook } from '@testing-library/react'
import React from 'react'
import { describe, expect, it, vi } from 'vitest'

import { MenuProvider, useMenu } from '../MenuProvider'

import { menuItemTestUtil } from './utils'

const menuData = [
  menuItemTestUtil('users', 'Users', true),
  menuItemTestUtil('products', 'Products', true),
]

describe('MenuContext context', () => {
  it('should throw an error if used outside provider', () => {
    // Silence the stack trace by mocking the consoles error object.
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    vi.spyOn(console, 'error').mockImplementation(() => {})
    expect(() => renderHook(() => useMenu())).toThrow(
      Error(
        'useMenu hook was called outside of context, make sure your app is wrapped with MenuProvider component'
      )
    )
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
