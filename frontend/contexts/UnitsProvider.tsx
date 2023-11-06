import { createContext, useContext, useMemo, type ReactNode } from 'react'

import { type UnitListOut } from '../types'

export interface UnitOption {
  label: string
  value: string
}

export interface UnitsContextType {
  units: UnitListOut[] | undefined
  unitsOptions: UnitOption[] | undefined
}

const UnitsContext = createContext<UnitsContextType | undefined>(undefined)

export function useUnits() {
  const ctx = useContext(UnitsContext)

  if (!ctx) {
    throw new Error(
      'useUnits hook was called outside of context, make sure your app is wrapped with UnitsProvider component'
    )
  }

  return ctx
}

interface UnitsProviderProps extends UnitsContextType {
  children: ReactNode
}

export function UnitsProvider({ units, unitsOptions, children }: UnitsProviderProps) {
  const value = useMemo(() => ({ units, unitsOptions }), [units, unitsOptions])
  return <UnitsContext.Provider value={value}>{children}</UnitsContext.Provider>
}
