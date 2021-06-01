import React, { useState } from "react";
import styled from "styled-components";
import { Form, Button } from "react-bootstrap";
import { GoogleLogin } from "react-google-login";
// import Logo from "./logos/CYOSLogo";
// import GoogleLogo from "./logos/GoogleLogo";
import axios from "axios";

const InLineText = styled(Form.Text)`
  font-size: ${(props) => props.fontSize};
  float: ${(props) => props.float};
  color: black;
  font-weight: bold;
  margin-bottom: 20px;
`;

const InLineATag = styled.a`
  font-size: ${(props) => props.fontSize};
  float: ${(props) => props.float};
  margin-bottom: 20px;
  color: #088771;
  font-weight: bold;
`;

const responseGoogle = (response) => {
  console.log(response);
};

const SignUp = () => {
  const [address, setAddress] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  const handlePassword = (e) => {
    console.log(e.target.value);
    setPassword(e.target.value);
  };

  const handleWalletAddress = (e) => {
    console.log(e.target.value);
    setAddress(e.target.value);
  };

  const handleFirstName = (e) => {
    console.log(e.target.value);
    setFirstName(e.target.value);
  };

  const handleLastName = (e) => {
    console.log(e.target.value);
    setLastName(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(address, password);

    try {
      const result = await axios.post("http://localhost:5000/auth/signup", {
        firstName: firstName,
        lastName: lastName,
        walletAddress: address,
        password: password,
      });
      const data = result.data;

      if (data.error) {
        console.log(
          "THERE WAS AN ERROR, SHOULD REDIRECT TO LOGIN AGAIN WITH AN ERROR MESSAGE"
        );
      } else if (data.data) {
        console.log("LOTS OF DATA: ", data.data.account);
      }
    } catch (err) {
      console.log("Unsuccessful Request: ", err);
    }
  };

  return (
    <div className="box">
      <div className="login-wrapper">
        <Form style={{ width: "350px" }}>
          <Form.Group controlId="formBasicEmail">
            <Form.Control
              placeholder="First Name"
              onChange={handleFirstName}
              required
              style={{border: "1px solid",   width: "100%", padding: "12px 20px", margin: "8px 0", boxSizing: "border-box"}}
            />
          </Form.Group>
          <Form.Group controlId="formBasicEmail">
            <Form.Control
              placeholder="Last Name"
              onChange={handleLastName}
              required
              style={{border: "1px solid",   width: "100%", padding: "12px 20px", margin: "8px 0", boxSizing: "border-box"}}
            />
          </Form.Group>
          <Form.Group controlId="formBasicEmail">
            <Form.Control
              placeholder="Enter Wallet Address"
              onChange={handleWalletAddress}
              required
              style={{border: "1px solid",   width: "100%", padding: "12px 20px", margin: "8px 0", boxSizing: "border-box"}}
            />
          </Form.Group>
          <Form.Group controlId="formBasicEmail">
            <Form.Control
              type="password"
              placeholder="Enter Password"
              onChange={handlePassword}
              required
              style={{border: "1px solid",   width: "100%", padding: "12px 20px", margin: "8px 0", boxSizing: "border-box"}}
            />
          </Form.Group>
          <Button
            variant="primary"
            type="submit"
            style={{
              width: "350px",
              backgroundColor: "#BBC918",
              border: "1px solid #BBC918",
            }}
            onClick={handleSubmit}
          >
            Sign In
          </Button>
        </Form>
        <GoogleLogin
          clientId="174084973781-lghmn9234jkpq2elgna0cd2hifg4tu5k.apps.googleusercontent.com"
          render={(renderProps) => (
            <button
              onClick={renderProps.onClick}
              style={{
                width: "350px",
                backgroundColor: "white",
                padding: "5px",
                border: "1px solid white",
                borderRadius: "5px",
              }}
            >
              Sign In With Google
            </button>
          )}
          buttonText="Login"
          onSuccess={responseGoogle}
          onFailure={responseGoogle}
          cookiePolicy={"single_host_origin"}
        />
      </div>
    </div>
  );
};

export default SignUp;
