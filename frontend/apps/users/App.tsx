/* eslint-disable react/prop-types */
import { Button, Menu, Title } from '@mantine/core'
import React, { useState } from 'react'
import { UserList, UserListAPIResponse } from '../../types/generated/dist'

import { IconEye } from '@tabler/icons-react'
import { MRT_RowSelectionState } from 'mantine-react-table'
import Table from '../../components/Table'
import View from '../../components/View'
import urls from './urls'
import { useFetch } from '../../hooks/fetcher'

interface UsersAppInnerProps {
  results: { users: UserListAPIResponse }
}

function UsersAppInner({ results }: UsersAppInnerProps) {
  const { users } = results
  const [selectedRows, setSelectedRows] = useState<MRT_RowSelectionState>({})

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title>Users</Title>
        <div className="flex items-center space-x-3">
          {Object.keys(selectedRows).length > 0 && (
            <Button.Group>
              <Button variant="default">Deactivate</Button>
              <Button variant="default">Delete</Button>
            </Button.Group>
          )}
          <Button>Add user</Button>
        </div>
      </div>

      <Table<UserList>
        rowIdentifier="id"
        columns={[
          { header: 'Id', accessorKey: 'id', size: 20 },
          { header: 'Name', accessorKey: 'fullName' },
          { header: 'Email', accessorKey: 'email' },
          { header: 'Home', accessorKey: 'home.address' },
          { header: 'Active', accessorKey: 'isActive', options: { isBoolean: true } },
          { header: 'Staff', accessorKey: 'isStaff', options: { isBoolean: true } },
        ]}
        data={users.data || []}
        onRowSelectionChange={setSelectedRows}
        actionMenuItems={({ row }) => [
          <Menu.Item key={1} icon={<IconEye />} onClick={() => console.info(row.id)}>
            Hijack
          </Menu.Item>,
        ]}
      />
    </div>
  )
}

function UsersApp() {
  const users = useFetch<UserListAPIResponse>(urls.list())

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
