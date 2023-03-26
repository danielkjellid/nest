import { Group, Header as MHeader, Menu, Stack, Text, UnstyledButton } from '@mantine/core'

import ColorSchemeSwitch from '../ColorSchemeSwitch'
import Logo from '../Logo'
import React from 'react'
import cx from 'classnames'
import { useCommonContext } from '../../state/CommonProvider'

interface HomeItemProps {
  address: string
  isActive: boolean
}

function HomeItem({ address, isActive }: HomeItemProps) {
  return (
    <Group spacing="xs" align="center">
      <div
        className={cx('h-2 w-2 rounded-full', {
          'bg-green-500': isActive,
          'bg-red-500': !isActive,
        })}
      />
      <Text fz="sm" className="font-medium">
        {address}
      </Text>
    </Group>
  )
}

function Header() {
  const { currentHome, availableHomes, setCurrentHome } = useCommonContext()

  return (
    <MHeader height={80}>
      <Stack
        sx={{ height: '100%' }}
        p="md"
        justify="space-between"
        align="center"
        className="flex-row"
      >
        <Logo className="h-12 w-12" />
        {currentHome &&
          (availableHomes.length ? (
            <Menu shadow="md">
              <Menu.Target>
                <UnstyledButton>
                  <HomeItem address={currentHome.address} isActive={currentHome.isActive} />
                </UnstyledButton>
              </Menu.Target>
              <Menu.Dropdown>
                {availableHomes.map((home) => (
                  <Menu.Item key={home.id} onClick={() => setCurrentHome(home)}>
                    <HomeItem address={home.address} isActive={home.isActive} />
                  </Menu.Item>
                ))}
              </Menu.Dropdown>
            </Menu>
          ) : (
            <HomeItem address={currentHome.address} isActive={currentHome.isActive} />
          ))}
        <ColorSchemeSwitch size="md" />
      </Stack>
    </MHeader>
  )
}

export default Header
