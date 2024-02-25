import { Heading, Tooltip } from "@chakra-ui/react";

export default function App() {
  return (
    <>
      <Heading>Crosslyric</Heading>
      <Tooltip label="Hey, I'm here!" aria-label="A tooltip">
        Hover me
      </Tooltip>
    </>
  );
}
