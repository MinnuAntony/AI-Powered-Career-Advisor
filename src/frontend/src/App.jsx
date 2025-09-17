
// import React from "react";
// import Home from "./pages/Home";

// export default function App() {
//   return <Home />;
// }
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import ChatBotPage from "./pages/ChatBotPage"; // new page

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chatbot" element={<ChatBotPage />} />
      </Routes>
    </Router>
  );
}
