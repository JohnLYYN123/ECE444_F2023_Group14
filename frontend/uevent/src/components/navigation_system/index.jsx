import React, {useCallback, useState} from 'react';
import {
    MenuFoldOutlined,
    MenuUnfoldOutlined,
    UserOutlined,
    ShoppingCartOutlined,
    UsergroupAddOutlined,
    LogoutOutlined,
    FolderAddOutlined
} from '@ant-design/icons';
import { Layout, Menu, Button, theme } from 'antd';
import MainPage from "../main_system";
import PostClub from "../main_system/post_club";
import Logout from "../user_authentication_system/logout";
import EnrollmentCart from "../enrollment_cart_system";
import PostEventForm from "../main_system/post_event";
const { Header, Sider, Content } = Layout;
const NavigationBar = () => {
    const [collapsed, setCollapsed] = useState(false);
    const {
        token: { colorBgContainer },
    } = theme.useToken();
    const [menuSelected, setMenuSelected] = useState('1');
    const onMenuClick = useCallback((e) => {
        setMenuSelected(e.key);
    }, [setMenuSelected]);

    const menuProvider = useCallback(() => {
        if (menuSelected === '1') {
            console.log('menuselected 1');
            return <MainPage/>;
        }
        else if (menuSelected === '2') {
            return <EnrollmentCart/>
        }
        else if (menuSelected === '3') {
            return <PostClub/>
        }
        else if (menuSelected === '4') {
            return <PostEventForm/>
        }
        else if (menuSelected === '5') {
            return <Logout/>
        }
        else {
            return <></>
        }
    }, [menuSelected]);

    return (
        <Layout>

            <Sider trigger={null} collapsible collapsed={collapsed}>
                <div className="demo-logo-vertical" />
                <Menu
                    theme="dark"
                    mode="inline"
                    defaultSelectedKeys={['1']}
                    items={[
                        {
                            key: '1',
                            icon: <UserOutlined />,
                            label: 'Dashboard',
                        },
                        {
                            key: '2',
                            icon: <ShoppingCartOutlined />,
                            label: 'Enrollment cart',
                        },
                        {
                            key: '3',
                            icon: <UsergroupAddOutlined />,
                            label: 'Add Club Info',
                        },
                        {
                            key: '4',
                            icon: <FolderAddOutlined />,
                            label: 'Post Event',
                        },
                        {
                            key: '5',
                            icon: <LogoutOutlined />,
                            label: 'Log out',
                        },
                    ]}
                    onClick={onMenuClick}
                />
            </Sider>
            <Layout>
                <Header
                    style={{
                        padding: 0,
                        background: colorBgContainer,
                    }}
                >
                    <Button
                        type="text"
                        icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
                        onClick={() => setCollapsed(!collapsed)}
                        style={{
                            fontSize: '16px',
                            width: 64,
                            height: 64,
                        }}
                    />
                </Header>
                <Content
                    style={{
                        margin: '24px 16px',
                        padding: 24,
                        minHeight: 500,
                        background: colorBgContainer,
                    }}
                >
                    {menuProvider()}
                </Content>
            </Layout>
        </Layout>

    );
};
export default NavigationBar;