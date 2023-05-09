import { createStyles } from '@mantine/core'

export const useCardStyles = createStyles((theme) => ({
  card: {
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[7] : '#fff',
  },
  tableHeader: {
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : '#f9fafb',
  },
}))
