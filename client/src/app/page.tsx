// app/page.tsx
"use client";
import { Link } from "@chakra-ui/next-js";
import Crossword from "@jaredreisinger/react-crossword";
import data from "./crossword";

export default function Home() {
  return (
    <>
      <Link href="/play" color="blue.400" _hover={{ color: "blue.500" }}>
        Play
      </Link>
      <Crossword data={data} />
    </>
  );
}
