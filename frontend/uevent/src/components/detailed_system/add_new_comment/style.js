import styled from "styled-components";
import { Link } from "react-router-dom";

export const Img = styled.img`
  display: block;
  width: 13%;
  margin: 20px auto 20px auto;
  @media (max-width: 1000px) {
    width: 30%;
  }
  @media (max-width: 650px) {
    width: 40%;
  }
  @media (max-width: 450px) {
    width: 50%;
  }
  @media (max-width: 350px) {
    width: 55%;
  }
`;

export const DivButtons = styled.div`
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
`;

export const ButtonBack = styled(Link)`
  display: block;
  border: 1px solid #1E90FF;
  border-radius: 10px;
  background: #fff;
  color: #1E90FF;
  text-decoration: none;
  padding: 6px 55px;
  transition: 0.4s;
  cursor: pointer;
  &:hover {
    background: #6495ED;
    color: #fff;
    transform: translateY(-2px);
    box-shadow: rgba(0, 0, 0, 0.12) 0 8px 15px;
  }
  &:active {
    opacity: 0.5;
  }
  @media (max-width: 375px) {
    padding: 10px 30px;
    font-size: 11px;
  }
`;


export const DivSingIn = styled.div`
  display: block;
  text-align: center;
  margin-top: 20px;
`;

export const LinkToLogin = styled(Link)`
  display: block;
  color: #000000;
  font-style: normal;
  font-weight: 500;
  margin-bottom: 30px;
  font-size: 13px;
  text-decoration: none;
  span {
    color: #1E90FF;
  }
  @media (max-width: 375px) {
    font-size: 10px;
  }
`;