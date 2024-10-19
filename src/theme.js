import { extendTheme } from "@chakra-ui/react";

const theme = extendTheme({
  fonts: {
    body: "Nunito, sans-serif",
    heading: "Nunito, sans-serif",
  },
  colors: {
    customColors: {
      darkGray: "#393B43",
      orange: "#D66B20",
      lightGray: "#E9EBF3",
    },
  },
});

export default theme;
