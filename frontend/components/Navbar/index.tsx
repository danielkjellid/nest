import { IconLogout, TablerIconsProps } from '@tabler/icons-react'
import { Navbar as MNavbar, Stack, Tooltip, UnstyledButton, createStyles } from '@mantine/core'
import React, { JSXElementConstructor } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

import apps from '../../apps/config'
import cx from 'classnames'
import { useMenu } from '../../contexts/MenuProvider'

const useStyles = createStyles((theme) => ({
  link: {
    color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7],

    '&:hover': {
      backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[5] : theme.primaryColor[0],
    },
  },

  active: {
    '&, &:hover': {
      backgroundColor:
        theme.colorScheme === 'dark'
          ? theme.fn.variant({ variant: 'dark', color: theme.primaryColor }).background
          : theme.fn.variant({ variant: 'light', color: theme.primaryColor }).background,
      color:
        theme.colorScheme === 'dark'
          ? theme.fn.variant({ variant: 'dark', color: theme.primaryColor }).color
          : theme.fn.variant({ variant: 'light', color: theme.primaryColor }).color,
    },
  },
}))

interface NavbarLinkProps {
  icon: JSXElementConstructor<TablerIconsProps>
  label: string
  active?: boolean
  onClick?(): void
}

function NavbarLink({ icon: Icon, label, active, onClick }: NavbarLinkProps) {
  const { classes } = useStyles()
  return (
    <Tooltip label={label} position="right" transitionProps={{ duration: 0 }}>
      <UnstyledButton
        className={cx(['w-12 h-12 rounded-md flex items-center opacity-90 p-3', classes.link], {
          [classes.active]: active,
        })}
        onClick={onClick}
      >
        <Icon className="w-8 h-8" />
      </UnstyledButton>
    </Tooltip>
  )
}

function Navbar() {
  const { menu } = useMenu()
  const location = useLocation()
  const navigate = useNavigate()

  const items = menu.map((menuItem) => {
    const correspondingApp = apps.find((app) => app.key === menuItem.key)

    if (!correspondingApp) {
      return
    }

    const { icon, path } = correspondingApp
    return (
      <NavbarLink
        key={menuItem.key}
        label={menuItem.title}
        active={location.pathname === path}
        icon={() => icon}
        onClick={() => navigate(path)}
      />
    )
  })

  return (
    <MNavbar width={{ base: 80 }} p="md">
      <MNavbar.Section grow>
        <Stack justify="center" spacing="sm">
          {items}
        </Stack>
      </MNavbar.Section>
      <MNavbar.Section>
        <Stack justify="center" spacing={0}>
          <NavbarLink icon={IconLogout} label="Logout" />
        </Stack>
      </MNavbar.Section>
    </MNavbar>
  )
}

export default Navbar
