import React, { createContext, useContext, useMemo } from 'react'

import { UnitListOut } from '../types'

export interface UnitsContextType {
  units: UnitListOut[] | undefined
  unitsOptions: { label: string; value: string }[] | undefined
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
  children: React.ReactNode
}

export function UnitsProvider({ units, unitsOptions, children }: UnitsProviderProps) {
  const value = useMemo(() => ({ units, unitsOptions }), [units, unitsOptions])
  return <UnitsContext.Provider value={value}>{children}</UnitsContext.Provider>
}
