import { MRT_ColumnDef, MantineReactTable } from 'mantine-react-table'

import React from 'react'
import View from '../../components/View'
import urls from './urls'
import { useFetch } from '../../hooks/fetcher'

interface TestResponse {
  id: number
}
interface UsersAppInnerProps {
  data?: TestResponse
}

function UsersAppInner({ data }: UsersAppInnerProps) {
  return (
    <div>
      <p>{JSON.stringify(data)}</p>
      <MantineReactTable
        columns={[
          { header: 'id', accessorKey: 'id' },
          { header: 'name', accessorKey: 'name' },
          { header: 'home', accessorKey: 'home' },
          { header: 'active', accessorKey: 'active' },
          { header: 'staff', accessorKey: 'staff' },
          { header: 'actions', accessorKey: 'actions' },
        ]}
        data={[
          {
            id: 1,
            name: 'Daniel',
            home: 'Vitaminveien 22',
            active: true,
            staff: true,
            actions: '',
          },
        ]}
      />
    </div>
  )
}

function UsersApp() {
  const users = useFetch(urls.test())

  return (
    <View<object, UsersAppInnerProps>
      component={UsersAppInner}
      results={{ users }}
      componentProps={{}}
      loadingProps={{ description: 'Testing' }}
    />
  )
}

export default UsersApp
