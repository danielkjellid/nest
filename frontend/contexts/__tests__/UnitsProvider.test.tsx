import { renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import { UnitType } from '../../types'
import { UnitsProvider, useUnits } from '../UnitsProvider'

import { unitItemTestUtil } from './utils'

const unitsData = [
  unitItemTestUtil(),
  unitItemTestUtil(2, 'Kilogram', 'kg', UnitType.Weight, 1000, false, false, 'Kilogram (kg)'),
]
const unitsOptions = unitsData.map((unit) => ({
  label: unit.displayName,
  value: unit.id.toString(),
}))

describe('UnitsContext context', () => {
  it('should throw an error if used outside provider', () => {
    // Silence the stack trace by mocking the consoles error object.
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    vi.spyOn(console, 'error').mockImplementation(() => {})
    expect(() => renderHook(() => useUnits())).toThrow(
      Error(
        'useUnits hook was called outside of context, make sure your app is wrapped with UnitsProvider component'
      )
    )
  })

  it('should respond gracefully when used inside provider', () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => {
      return (
        <UnitsProvider units={unitsData} unitsOptions={unitsOptions}>
          {children}
        </UnitsProvider>
      )
    }

    const { result } = renderHook(() => useUnits(), { wrapper: wrapper })

    expect(result.current).toStrictEqual({
      units: [
        {
          id: 1,
          name: 'Gram',
          abbreviation: 'g',
          unitType: UnitType.Weight,
          baseFactor: 1,
          isBaseUnit: true,
          isDefault: true,
          displayName: 'Gram (g)',
        },
        {
          id: 2,
          name: 'Kilogram',
          abbreviation: 'kg',
          unitType: UnitType.Weight,
          baseFactor: 1000,
          isBaseUnit: false,
          isDefault: false,
          displayName: 'Kilogram (kg)',
        },
      ],
      unitsOptions: [
        { label: 'Gram (g)', value: '1' },
        { label: 'Kilogram (kg)', value: '2' },
      ],
    })
  })
})
