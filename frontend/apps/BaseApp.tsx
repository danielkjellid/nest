import {
  AppShell,
  ColorScheme,
  ColorSchemeProvider,
  MantineProvider,
  createEmotionCache,
} from '@mantine/core'
import { useHotkeys, useLocalStorage } from '@mantine/hooks'

import { Notifications } from '@mantine/notifications'
import React from 'react'

interface BaseAppProps {
  appShellClassName?: string
  navbar?: React.ReactElement
  header?: React.ReactElement
  children: React.ReactNode
}

function BaseApp({ appShellClassName, navbar, header, children }: BaseAppProps) {
  /********************
   ** Provider cache **
   ********************/

  // Append Mantine css last to not interfere/overwrite tailwind styles.
  const emotionCache = createEmotionCache({ key: 'mantine', prepend: true })

  /******************
   ** Color scheme **
   ******************/

  const [colorScheme, setColorScheme] = useLocalStorage<ColorScheme>({
    key: 'color-scheme',
    defaultValue: 'light',
    getInitialValueInEffect: true,
  })
  const toggleColorScheme = (value?: ColorScheme) =>
    setColorScheme(value || (colorScheme === 'dark' ? 'light' : 'dark'))

  /*************
   ** Hotkeys **
   *************/

  useHotkeys([['mod+J', () => toggleColorScheme()]])

  return (
    <ColorSchemeProvider colorScheme={colorScheme} toggleColorScheme={toggleColorScheme}>
      <MantineProvider
        emotionCache={emotionCache}
        withGlobalStyles
        withNormalizeCSS
        theme={{
          colorScheme,
          primaryColor: 'violet',
          fontFamily: 'Inter, sans-serif;',
        }}
      >
        <AppShell
          className={appShellClassName}
          navbar={navbar}
          header={header}
          styles={(theme) => ({
            main: {
              color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.dark[8],
              backgroundColor:
                theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[0],
            },
          })}
        >
          <Notifications />
          {children}
        </AppShell>
      </MantineProvider>
    </ColorSchemeProvider>
  )
}

export default BaseApp
