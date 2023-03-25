import { IconMoon, IconSun } from '@tabler/icons-react'
import { MantineSize, Switch, useMantineColorScheme, useMantineTheme } from '@mantine/core'

import React from 'react'

interface ColorSchemeSwitchProps {
  size: MantineSize
}

function ColorSchemeSwitch({ size }: ColorSchemeSwitchProps) {
  /****************************
   ** Theme and color scheme **
   ****************************/
  const theme = useMantineTheme()
  const { colorScheme, toggleColorScheme } = useMantineColorScheme()

  return (
    <Switch
      checked={colorScheme === 'dark'}
      onChange={() => toggleColorScheme()}
      size={size}
      onLabel={<IconSun className="h-12" color={theme.white} />}
      offLabel={<IconMoon className="h-12" color={theme.colors.gray[6]} />}
    />
  )
}

export default ColorSchemeSwitch
