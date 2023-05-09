import { createStyles } from '@mantine/core'

export const useProductDetailStyles = createStyles((theme) => ({
  changeMessageCode: {
    backgroundColor:
      theme.colorScheme === 'dark'
        ? theme.fn.rgba(theme.colors[theme.primaryColor][9], 0.45)
        : theme.colors[theme.primaryColor][0],
    color:
      theme.colorScheme === 'dark'
        ? theme.colors[theme.primaryColor][1]
        : theme.colors[theme.primaryColor][8],
  },
}))
