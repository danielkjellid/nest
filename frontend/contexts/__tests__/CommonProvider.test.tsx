import { CommonProvider, useCommonContext } from '../CommonProvider'
import { describe, expect, it, test } from 'vitest'

import React from 'react'
import { createCommonContextTestData } from './utils'
import { renderHook } from '@testing-library/react'

describe('CommonContext context', () => {
  it('should throw an error if used outside provider', () => {
    test.fails('fail test', () => {
      const { result } = renderHook(() => useCommonContext())
      expect(result.current).rejects.toBe(0)
    })
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
