import { Heading, Tooltip } from "@chakra-ui/react";

import Crossword from "@jaredreisinger/react-crossword";

const data = {
  across: {
    1: {
      clue: "one plus one",
      answer: "TWO",
      row: 0,
      col: 0,
    },
  },
  down: {
    2: {
      clue: "three minus two",
      answer: "ONE",
      row: 0,
      col: 2,
    },
  },
};

export default function App() {
  return (
    <>
      <Heading>Crosslyric</Heading>
      <Tooltip label="Hey, I'm here!" aria-label="A tooltip">
        Hover me
      </Tooltip>
      <Crossword data={data} />;
    </>
  );
}
