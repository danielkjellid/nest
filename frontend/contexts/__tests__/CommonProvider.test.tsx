import { renderHook } from '@testing-library/react'
import React from 'react'
import { describe, expect, it, vi } from 'vitest'

import { CommonProvider, useCommonContext } from '../CommonProvider'


import { createCommonContextTestData } from './utils'


describe('CommonContext context', () => {
  it('should throw an error if used outside provider', () => {
    // Silence the stack trace by mocking the consoles error object.
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    vi.spyOn(console, 'error').mockImplementation(() => {})
    expect(() => renderHook(() => useCommonContext())).toThrow(
      Error(
        'useCommonContext hook was called outside of context, make sure your app is wrapped with CommonProvider component'
      )
    )
  })

  it('should respond gracefully when used inside provider', () => {
    const { config, currentHome, currentUser, availableHomes } = createCommonContextTestData()
    const wrapper = ({ children }: { children: React.ReactNode }) => {
      return (
        <CommonProvider
          config={config}
          currentHome={currentHome}
          currentUser={currentUser}
          availableHomes={availableHomes}
          setCurrentHome={() => console.log('set home')}
        >
          {children}
        </CommonProvider>
      )
    }

    const { result } = renderHook(() => useCommonContext(), { wrapper })

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { setCurrentHome: _, ...contextWithoutHandler } = result.current

    expect(contextWithoutHandler).toStrictEqual({
      config,
      currentHome,
      currentUser,
      availableHomes,
    })
  })
})
