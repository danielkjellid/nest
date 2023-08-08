import { createStyles } from '@mantine/core'

export const useTableStyles = createStyles((theme) => ({
  rowBackground: {
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[7] : '#fff',
    '&:nth-of-type(even)': {
      backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[8] : '#F3F4F6',
    },
  },
}))
