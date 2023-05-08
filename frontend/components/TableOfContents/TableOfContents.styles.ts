import { createStyles, rem } from '@mantine/core'

export const useTableOfContentsStyles = createStyles((theme) => ({
  wrapper: {
    boxSizing: 'border-box',
    position: 'sticky',
    right: 0,
    flex: `0 0 ${rem(260 - 20)}`,
  },

  withTabs: {
    paddingTop: 0,
    top: `calc(${rem(60)} + ${theme.spacing.xl})`,
  },

  inner: {
    paddingTop: 0,
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
  },

  items: {
    borderLeft: `${rem(2)} solid ${
      theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[2]
    }`,
  },

  link: {
    display: 'block',
    color: theme.colorScheme === 'dark' ? theme.colors.dark[1] : theme.colors.gray[7],
    borderLeft: `${rem(2)} solid transparent`,
    padding: `${rem(8)} ${theme.spacing.md}`,
    marginLeft: -1,
  },

  linkActive: {
    borderLeftColor: theme.colors[theme.primaryColor][5],
    backgroundColor:
      theme.colorScheme === 'dark'
        ? theme.fn.rgba(theme.colors[theme.primaryColor][9], 0.45)
        : theme.colors[theme.primaryColor][0],
    color:
      theme.colorScheme === 'dark'
        ? theme.colors[theme.primaryColor][1]
        : theme.colors[theme.primaryColor][8],
  },

  header: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: theme.spacing.md,
  },
}))
