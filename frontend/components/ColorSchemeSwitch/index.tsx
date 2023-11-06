import { ActionIcon, useMantineColorScheme, useMantineTheme } from '@mantine/core'
import { IconMoon, IconSun } from '@tabler/icons-react'

function ColorSchemeSwitch() {
  /****************************
   ** Theme and color scheme **
   ****************************/

  const theme = useMantineTheme()
  const { colorScheme, toggleColorScheme } = useMantineColorScheme()

  return (
    <ActionIcon size="lg" radius="md" variant="default" onClick={() => toggleColorScheme()}>
      {colorScheme === 'dark' ? (
        <IconSun color={theme.colors.gray[1]} stroke={1.5} className="w-5 h-5" />
      ) : (
        <IconMoon color={theme.colors.gray[7]} stroke={1.5} className="w-5 h-5" />
      )}
    </ActionIcon>
  )
}

export default ColorSchemeSwitch
