import { createStyles } from '@mantine/core'

export const useCommonStyles = createStyles((theme) => ({
  border: {
    borderColor: theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[2],
  },
  title: {
    color: theme.colorScheme === 'dark' ? theme.colors.gray[3] : theme.colors.gray[9],
  },
  subtitle: {
    color: theme.colorScheme === 'dark' ? theme.colors.dark[1] : theme.colors.gray[7],
  },
  iconSuccess: {
    color: theme.colors.green[5],
  },
  iconDanger: {
    color: theme.colors.red[5],
  },
}))
