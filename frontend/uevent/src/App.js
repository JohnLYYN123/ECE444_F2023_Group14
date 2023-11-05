import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "./components/user_authentication_system/login";
import RegisterForm from "./components/user_authentication_system/registration";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterForm />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
