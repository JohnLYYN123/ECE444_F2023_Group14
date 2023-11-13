import React, { useCallback, useState, useEffect } from 'react';
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
import EnrollmentCart from "../enrollment_cart_system";
import PostEventForm from "../main_system/post_event";
import './navigation_system.css';

const { Header, Sider, Content } = Layout;

const NavigationBar = () => {
    const [collapsed, setCollapsed] = useState(false);
    const {
        token: { colorBgContainer },
    } = theme.useToken();
    const [menuSelected, setMenuSelected] = useState('1');
    const onMenuClick = useCallback((e) => {
        console.log(e);
        setMenuSelected(e.key);
    }, [setMenuSelected]);

    useEffect(() => {
        const handleLogout = async () => {
            try {
                const response = await fetch('http://ece444uevent.pythonanywhere.com/user/logout', {
                    mode: "cors",
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `${window.localStorage['token']}`
                    },
                });

                if (response.ok) {
                    console.log('Logout successful');
                    window.localStorage.removeItem("token");
                    // Redirect to the homepage or another desired page
                    window.location.href = '/login';
                    alert('Thank you for your visiting');
                } else {
                    const errorData = await response.json();
                    const code = errorData.code;
                    const message = errorData.error || 'Unknown error';
                    if (code == "401" & message == "Authentication is required to access this resource") {
                        // Redirect to the homepage or another desired page
                        alert('Please log in to continue.');
                        window.location.href = '/login';
                    }
                    alert('Error happens. Please try again later.');
                }
            } catch (error) {
                alert('Error happens. Please try again later.');
            }
        };
        if (menuSelected === '5') {
            handleLogout();
        }
    }, [menuSelected]);

    const menuProvider = useCallback(() => {
        if (menuSelected === '1') {
            return <MainPage />;
        }
        else if (menuSelected === '2') {
            return <EnrollmentCart />
        }
        else if (menuSelected === '3') {
            return <PostClub />
        }
        else if (menuSelected === '4') {
            return <PostEventForm />
        }
        // else if (menuSelected === '5') {
        //     handleLogout();
        // }
        else {
            return <></>
        }
    }, [menuSelected]);

    return (
        <Layout className="navigation-layout">

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
                <Content className='navigation-content'>
                    {menuProvider()}
                </Content>
            </Layout>
        </Layout>

    );
};
export default NavigationBar;