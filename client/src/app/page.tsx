// app/page.tsx
"use client";
import Crossword from "@jaredreisinger/react-crossword";
import data from "./crossword";
import { Box, Center, Heading, Text, VStack } from "@chakra-ui/react";
import Player from "./Player";

export default function Home() {
  return (
    <>
      <Center m="2em">
        <VStack>
          <Heading>Crosslyric</Heading>
          <Heading size="l">The crossword for your ears.</Heading>
        </VStack>
      </Center>
      <Box m="4em">
        <Crossword data={data} />
      </Box>
      <VStack>
        <Text>1:</Text> <Player path="1.wav" />
        <Text>2:</Text> <Player path="2.wav" />
        <Text>3:</Text> <Player path="3.wav" />
        <Text>4:</Text> <Player path="4.wav" />
        <Text>5:</Text> <Player path="5.wav" />
        <Text>6:</Text> <Player path="6.wav" />
        <Text>7:</Text> <Player path="7.wav" />
        <Text>8:</Text> <Player path="8.wav" />
        <Text>9:</Text> <Player path="9.wav" />
        <Text>10: </Text>
        <Player path="10.wav" />
      </VStack>
    </>
  );
}
