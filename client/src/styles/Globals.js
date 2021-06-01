import { createGlobalStyle } from "styled-components";

export const Globals = createGlobalStyle`
    body {
        margin: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
        'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
        sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        background-color: white;
    }
    
    code {
        font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
        monospace;
    }
    // .box {
    //     display: flex;
    //     align-items: center;
    //     justify-content: center;
    //     padding: 100px 0;
    //     flex-direction: column;
    //   }
    // .login-wrapper {
    //     display: flex;
    //     flex-direction: column;
    //     align-items: center;
    //     background-color: #F2F2F2;
    //     padding: 25px;
    //     border: 2px solid #F2F2F2;
    //     border-radius: 10px;
    // }
`

export default Globals;