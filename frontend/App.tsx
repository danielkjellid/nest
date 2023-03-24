import { Layout, Menu, theme } from 'antd'
import { MenuFoldOutlined, MenuUnfoldOutlined, UploadOutlined } from '@ant-design/icons'
import React, { useState } from 'react'

const { Header, Footer, Sider, Content } = Layout

interface AppProps {
    test: number
}

declare global {
    interface Window {
        initialProps: AppProps;
    }
}

function App(props: AppProps) {
  const [collapsed, setCollapsed] = useState(false)
  const {
    token: { colorBgContainer },
  } = theme.useToken()

  console.log(props)

  return (
    <Layout className="min-h-screen">
      <Sider trigger={null} collapsible collapsed={collapsed}>
        <div className="h-16 bg-gray-200">Logo</div>
        <Menu
          theme="dark"
          mode="inline"
          items={[
            { key: 1, icon: <UploadOutlined />, label: 'nav 1' },
            { key: 2, icon: <UploadOutlined />, label: 'nav 2' },
          ]}
        />
      </Sider>
      <Layout>
        <Header style={{ background: colorBgContainer }}>
          {React.createElement(collapsed ? MenuUnfoldOutlined : MenuFoldOutlined, {
            className: 'trigger',
            onClick: () => setCollapsed(!collapsed),
          })}
        </Header>
        <Content>Content</Content>
        <Footer>Footer</Footer>
      </Layout>
    </Layout>
  )
}

export default App
