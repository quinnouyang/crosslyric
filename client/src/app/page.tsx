// app/page.tsx
"use client";
import { Link } from "@chakra-ui/next-js";
import Crossword from "@jaredreisinger/react-crossword";

export default function Home() {
  return (
    <>
      <Link href="/play" color="blue.400" _hover={{ color: "blue.500" }}>
        Play
      </Link>
      <Crossword
        data={{
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
        }}
      />
    </>
  );
}
