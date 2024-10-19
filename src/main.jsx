import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import { ChakraProvider } from "@chakra-ui/react";
import theme from "./theme";

createRoot(document.getElementById("root")).render(
  <ChakraProvider theme={theme}>
    <App />
  </ChakraProvider>
);
