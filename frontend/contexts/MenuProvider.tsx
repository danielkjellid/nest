import React, { createContext, useContext, useMemo } from 'react'

interface MenuItem {
  key: string
  title: string
  end: boolean
}

export interface MenuContextType {
  menu: MenuItem[]
}

const MenuContext = createContext<MenuContextType | null>(null)

export function useMenu() {
  const ctx = useContext(MenuContext)

  if (!ctx) {
    throw new Error(
      'useMenu hook was called outside of context, make sure your app is wrapped with MenuProvider component'
    )
  }

  return ctx
}

interface MenuProviderProps extends MenuContextType {
  children: React.ReactNode
}

export function MenuProvider({ menu, children }: MenuProviderProps) {
  const value = useMemo(() => ({ menu }), [menu])
  return <MenuContext.Provider value={value}>{children}</MenuContext.Provider>
}
