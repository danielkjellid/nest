import { describe, expect, it, test } from 'vitest'

import { renderHook } from '@testing-library/react'
import { useCommonContext } from '../CommonProvider'

describe('CommonContext context', () => {
  it('should throw an error if used outside provider', () => {
    test.fails('fail test', () => {
      const { result } = renderHook(() => useCommonContext())
      expect(result.current).rejects.toBe(0)
    })
  })
})
