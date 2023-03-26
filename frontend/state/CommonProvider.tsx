import React, { createContext, useContext } from 'react'

interface Home {
  id: number
  address: string
  numResidents: number
  numWeeksRecipeRotation: number
  weeklyBudget: number
  isActive: boolean
}

interface User {
  id: number
  email: string
  firstName: string
  lastName: string
  fullName: string
  isActive: boolean
  isStaff: boolean
  isSuperuser: boolean
  home?: Home
}

interface Config {
  isProduction: boolean
}

export interface CommonContextType {
  config: Config
  currentUser: User
  currentHome: Home
  availableHomes: Home[]
  setCurrentHome(home: Home): void
}

const CommonContext = createContext<CommonContextType | null>(null)

export function useCommonContext() {
  const ctx = useContext(CommonContext)

  if (!ctx) {
    throw new Error(
      'useCommonContext hook was called outside of context, make sure your app is wrapped with CommonProvider component'
    )
  }

  return ctx
}

interface CommonProviderProps extends CommonContextType {
  children: React.ReactNode
}

export function CommonProvider({
  config,
  currentUser,
  currentHome,
  availableHomes,
  setCurrentHome,
  children,
}: CommonProviderProps) {
  return (
    <CommonContext.Provider
      value={{ config, currentUser, currentHome, availableHomes, setCurrentHome }}
    >
      {children}
    </CommonContext.Provider>
  )
}
