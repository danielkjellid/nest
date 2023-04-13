import {
  Button,
  Card,
  Center,
  Container,
  PasswordInput,
  Stack,
  TextInput,
  Title,
} from '@mantine/core'
import React, { useEffect } from 'react'

import { BaseAppCore } from '../../components/BaseApp/BaseApp'
import ColorSchemeSwitch from '../../components/ColorSchemeSwitch'
import Logo from '../../components/Logo'
import { notifications } from '@mantine/notifications'
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

function LoginAppInner() {
  /**********
   ** Form **
   **********/

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
    <>
      <Container size="xs">
        <div className="absolute right-0 top-0 m-4">
          <ColorSchemeSwitch size="lg" />
        </div>
      </Container>
      <Container className="min-h-screen items-center flex justify-center" size="xs">
        <Stack>
          <Center>
            <Stack>
              <Logo className="h-16 w-16 mx-auto" />
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
    </>
  )
}

function LoginApp() {
  return (
    <BaseAppCore appShellClassName="fixed inset-0">
      <LoginAppInner />
    </BaseAppCore>
  )
}

export default LoginApp
