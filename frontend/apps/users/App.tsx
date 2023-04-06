/* eslint-disable react/prop-types */
import { Button, Menu, Title } from '@mantine/core'
import { UserList, UserListAPIResponse } from '../../types/generated/dist'

import { IconEye } from '@tabler/icons-react'
import React from 'react'
import Table from '../../components/Table'
import View from '../../components/View'
import urls from './urls'
import { useFetch } from '../../hooks/fetcher'

interface UsersAppInnerProps {
  results: { users: UserListAPIResponse }
}

function UsersAppInner({ results }: UsersAppInnerProps) {
  const { users } = results

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title>Users</Title>
        <Button>Add user</Button>
      </div>

      <Table<UserList>
        rowIdentifier="id"
        columns={[
          { header: 'Id', accessorKey: 'id', size: 20, enableEditing: false },
          { header: 'Name', accessorKey: 'fullName' },
          { header: 'Email', accessorKey: 'email' },
          { header: 'Home', accessorKey: 'home.address' },
          { header: 'Active', accessorKey: 'isActive', options: { isBoolean: true } },
          { header: 'Staff', accessorKey: 'isStaff', options: { isBoolean: true } },
        ]}
        data={users.data || []}
        actionMenuItems={({ row }) => [
          <Menu.Item key={2} icon={<IconEye />} onClick={() => console.info('Hijack')}>
            Hijack
          </Menu.Item>,
        ]}
      />
    </div>
  )
}

function UsersApp() {
  const users = useFetch<UserListAPIResponse>(urls.test())

  return (
    <View<object, UsersAppInnerProps>
      component={UsersAppInner}
      results={{ users }}
      componentProps={{}}
      loadingProps={{ description: 'Loading users...' }}
      errorProps={{ description: 'There was an error getting users. Please try again.' }}
    />
  )
}

export default UsersApp
