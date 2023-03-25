import {
  AppShell,
  Button,
  Card,
  Center,
  ColorScheme,
  ColorSchemeProvider,
  Container,
  MantineProvider,
  PasswordInput,
  Stack,
  Switch,
  Text,
  TextInput,
  Title,
  createEmotionCache,
  useMantineTheme,
} from '@mantine/core'
import { IconMoon, IconSun } from '@tabler/icons-react'
import { Notifications, notifications } from '@mantine/notifications'
import React, { useEffect } from 'react'
import { useHotkeys, useLocalStorage } from '@mantine/hooks'

import { useForm } from '@mantine/form'

declare global {
  interface Window {
    loginErrors?: boolean
    csrfToken: string
  }
}

interface LoginFormValues {
  email: string
  password: string
}

function LoginApp() {
  const emotionCache = createEmotionCache({ key: 'mantine', prepend: false })
  const [colorScheme, setColorScheme] = useLocalStorage<ColorScheme>({
    key: 'color-scheme',
    defaultValue: 'light',
    getInitialValueInEffect: true,
  })
  const theme = useMantineTheme()
  const toggleColorScheme = (value?: ColorScheme) =>
    setColorScheme(value || (colorScheme === 'dark' ? 'light' : 'dark'))

  useHotkeys([['mod+J', () => toggleColorScheme()]])

  const form = useForm<LoginFormValues>({ initialValues: { email: '', password: '' } })

  useEffect(() => {
    if (window.loginErrors) {
      form.setErrors({ email: 'Wrong email or password', password: 'Wrong email or password' })
      notifications.show({
        title: 'Wrong email or password!',
        message: 'Note that you have to separate between lowercase and uppercase characters',
        color: 'red',
      })
    }
  }, [window.loginErrors])

  return (
    <ColorSchemeProvider colorScheme={colorScheme} toggleColorScheme={toggleColorScheme}>
      <MantineProvider
        emotionCache={emotionCache}
        theme={{ colorScheme, primaryColor: 'violet', fontFamily: 'Inter, sans-serif;' }}
      >
        <AppShell
          className="fixed inset-0"
          styles={(theme) => ({
            main: {
              backgroundColor:
                theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[0],
            },
          })}
        >
          <Notifications />
          <div className="relative">
            <div className="absolute right-0 top-0 m-4">
              <Switch
                checked={colorScheme === 'dark'}
                onChange={() => toggleColorScheme()}
                size="lg"
                onLabel={<IconSun className="h-12" color={theme.white} />}
                offLabel={<IconMoon className="h-12" color={theme.colors.gray[6]} />}
              />
            </div>
            <Container className="min-h-screen items-center flex" size="xs">
              <Stack>
                <Center>
                  <Stack>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="64"
                      height="64"
                      fill="none"
                      className="mx-auto"
                    >
                      <g clipPath="url(#a)">
                        <rect width="64" height="64" fill="#7950F2" rx="8" />
                        <path
                          fill="#fff"
                          d="M22.071 47.48c-1.2 0-2.12-.32-2.76-.96-.64-.68-.96-1.64-.96-2.88V20.96c0-1.24.32-2.18.96-2.82.64-.64 1.54-.96 2.7-.96 1.16 0 2.06.32 2.7.96.64.64.96 1.58.96 2.82v4.08l-.66-1.5c.88-2.12 2.24-3.72 4.08-4.8 1.88-1.12 4-1.68 6.36-1.68 2.36 0 4.3.44 5.82 1.32 1.52.88 2.66 2.22 3.42 4.02.76 1.76 1.14 4 1.14 6.72v14.52c0 1.24-.32 2.2-.96 2.88-.64.64-1.56.96-2.76.96-1.2 0-2.14-.32-2.82-.96-.64-.68-.96-1.64-.96-2.88V29.48c0-2.28-.44-3.94-1.32-4.98-.84-1.04-2.16-1.56-3.96-1.56-2.2 0-3.96.7-5.28 2.1-1.28 1.36-1.92 3.18-1.92 5.46v13.14c0 2.56-1.26 3.84-3.78 3.84Z"
                        />
                      </g>
                      <defs>
                        <clipPath id="a">
                          <rect width="64" height="64" fill="#fff" rx="8" />
                        </clipPath>
                      </defs>
                    </svg>
                    <Title order={2}>Sign in to your account</Title>
                  </Stack>
                </Center>
                <Card withBorder radius="md" className="w-96">
                  <form method="POST">
                    <input name="csrfmiddlewaretoken" type="hidden" value={window.csrfToken} />
                    <Stack>
                      <TextInput
                        name="username"
                        label="Email"
                        required
                        {...form.getInputProps('email')}
                      />
                      <PasswordInput
                        name="password"
                        label="Password"
                        required
                        {...form.getInputProps('password')}
                      />
                      <Button size="md" type="submit">
                        Log in
                      </Button>
                    </Stack>
                  </form>
                </Card>
              </Stack>
            </Container>
          </div>
        </AppShell>
      </MantineProvider>
    </ColorSchemeProvider>
  )
}

export default LoginApp
