import { createStyles } from '@mantine/core'

export const useCommonStyles = createStyles((theme) => ({
  border: {
    borderColor: theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[2],
  },
  title: {
    color: theme.colorScheme === 'dark' ? theme.colors.gray[3] : theme.colors.gray[7],
  },
  subtitle: {
    color: theme.colorScheme === 'dark' ? theme.colors.dark[1] : theme.colors.gray[7],
  },
  muted: {
    color: theme.colorScheme === 'dark' ? theme.colors.gray[5] : theme.colors.gray[6],
  },
  iconSuccess: {
    color: theme.colors.green[5],
  },
  iconDanger: {
    color: theme.colors.red[5],
  },
  panel: {
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[7] : '#fff',
  },
  icon: {
    color: theme.colorScheme === 'dark' ? theme.colors.dark[2] : theme.colors.gray[6],
    '&:hover': {
      color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7],
    },
  },
}))
