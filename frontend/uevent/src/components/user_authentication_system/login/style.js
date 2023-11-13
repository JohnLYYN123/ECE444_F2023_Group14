import styled from "styled-components";
import { Link } from "react-router-dom";

export const Container = styled.div`
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;

    p {
        text-align: center;
        color: #1d164d;
        margin-bottom: 15px;
        font-size: 26px;
        font-weight: 600;
        @media (max-width: 375px){
            font-size: 20px;
        }
    }

    input {
        display:block;
        width: 320px;
        height: 45px;
        border: none;
        border-radius: 10px;
        box-shadow: -4px 4px 18px rgba(0, 0, 0, 0.09);
        color: #969696;
        margin: 10px auto 12px;
        padding: 0 15px;
        outline:none;
        cursor: pointer;
        @media (max-width: 375px){
            width: 250px;
            height: 35px;
            font-size: 11px;
        }
    }
`

export const Img = styled.img`
    display:block;
    width: 25%;
    margin: 20px auto 20px auto;
    @media (max-width:1000px){
            width: 35%;
    }
    @media (max-width: 850px){
        width: 45%;
    }
    @media (max-width: 650px){
        width: 55%;
    }
    @media (max-width: 450px){
        width: 60%;
    }
    @media (max-width: 350px){
        width: 62%;
    }
`;

export const Directions = styled.div`
    display: block;
    text-align: center;
    padding-left: 110px;
    font-size: 13px;
    margin-top: -10px;
    @media (max-width: 375px){
        padding-left: 110px;
        font-size: 9px;
    }
`;

export const ForgotPassword = styled(Link)`
    display:block;
    color:#000000;
    font-style: normal;
    font-weight: 500;
    text-decoration:none;
    padding-left: 88px;
    margin-top: 6px;
    cursor: pointer;
    @media (max-width: 375px){
        padding-left: 60px;
    }
`;

export const DivButtons = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-top: 20px;
    @media (max-width: 375px){
        gap: 10px;
    }
`;

export const ButtonBack = styled(Link)`
    display:block;
    border: 1px solid #1E90FF;
    border-radius: 10px;
    background: #fff;
    color: #1E90FF;
    text-decoration: none;
    padding: 15px 55px;
    transition: 0.4s;
    cursor: pointer;
    &:hover{
        background: #1E90FF;
        color: #fff;
        transform: translateY(-2px);
        box-shadow: rgba(0, 0, 0, 0.12) 0 8px 15px;
    }
    &:active{
        opacity: 0.5;
    }
    @media (max-width: 375px){
        padding: 5px 35px;
    }
`;


export const ButtonSend = styled.button`
    display:block;
    border: none;
    border-radius: 10px;
    background: #1E90FF;
    color: #FFFFFF;
    padding: 15px 55px;
    transition: all 300ms cubic-bezier(.23, 1, 0.32, 1);
    cursor: pointer;
    &:hover{
        transform: translateY(-2px);
        box-shadow: rgba(0, 0, 0, 0.12) 0 8px 15px;
    }
    &:active{
        opacity: 0.5;
    }
    @media (max-width: 375px){
        padding: 5px 35px;
    }
`;

export const DivRegister = styled.div`
    display: block;
    text-align: center;
    margin-top: 20px;
`;

export const LinkToRegister = styled(Link)`
    display:block;
    color:#000000;
    font-style: normal;
    font-weight: 500;
    margin-bottom: 5px;
    font-size: 15px;
    text-decoration:none;
    span {
        color: #1E90FF
    }
`;

