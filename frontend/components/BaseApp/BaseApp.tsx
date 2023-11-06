import {
  Alert,
  AppShell,
  ColorScheme,
  ColorSchemeProvider,
  MantineProvider,
  Text,
  UnstyledButton,
  createEmotionCache,
} from '@mantine/core'
import { useHotkeys, useLocalStorage } from '@mantine/hooks'
import { Notifications } from '@mantine/notifications'
import { IconInfoCircle } from '@tabler/icons-react'
import React from 'react'

import { useCommonContext } from '../../contexts/CommonProvider'

interface BaseAppCoreProps {
  appShellClassName?: string
  navbar?: React.ReactElement
  header?: React.ReactElement
  children: React.ReactNode
}

export function BaseAppCore({ appShellClassName, navbar, header, children }: BaseAppCoreProps) {
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
          primaryColor: 'green',
          fontFamily: 'Inter, sans-serif;',
          loader: 'dots',
        }}
      >
        <AppShell
          className={appShellClassName}
          navbar={navbar}
          header={header}
          padding={32}
          styles={(theme) => ({
            main: {
              color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.dark[8],
              backgroundColor:
                theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[0],
              minHeight: '100vh',
            },
          })}
        >
          <Notifications />
          <div className="max-w-7xl h-full mx-auto">{children}</div>
        </AppShell>
      </MantineProvider>
    </ColorSchemeProvider>
  )
}

interface BaseAppProps {
  appShellClassName?: string
  navbar?: React.ReactElement
  header?: React.ReactElement
  children: React.ReactNode
}
function BaseApp({ appShellClassName, navbar, header, children }: BaseAppProps) {
  /**********
   ** User **
   **********/

  const { currentUser } = useCommonContext()

  return (
    <BaseAppCore appShellClassName={appShellClassName} navbar={navbar} header={header}>
      <div className="h-full space-y-5">
        {currentUser && currentUser.isHijacked && (
          <Alert color="orange" title="User hijacked" icon={<IconInfoCircle className="w-5 h-5" />}>
            <div className="flex items-center justify-between">
              You&apos;re currently working on behalf of {currentUser.fullName}.
              <form action="/hijack/release/" method="post">
                <input name="csrfmiddlewaretoken" type="hidden" value={window.csrfToken} />
                <UnstyledButton type="submit">
                  <Text fz="sm" fw="bold" color="orange">
                    Release
                  </Text>
                </UnstyledButton>
              </form>
            </div>
          </Alert>
        )}
        <div className="h-full">{children}</div>
      </div>
    </BaseAppCore>
  )
}

export default BaseApp
