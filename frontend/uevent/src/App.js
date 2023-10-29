import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./components/user_authentication_system/login";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
