import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import { ChakraProvider, extendTheme } from "@chakra-ui/react";

const colors = {
  brand: {
    900: "#1a365d",
    800: "#153e75",
    700: "#2a69ac",
  },
  fonts: {
    heading: `Inter, sans-serif`,
    body: `Inter, sans-serif`,
    mono: `Menlo, monospace`,
  },
};

const theme = extendTheme({ colors });
const rootElement = document.getElementById("root");

if (rootElement)
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <ChakraProvider theme={theme}>
        <App />
      </ChakraProvider>
    </React.StrictMode>,
  );
