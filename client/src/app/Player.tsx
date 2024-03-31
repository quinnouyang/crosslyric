import { BellIcon } from "@chakra-ui/icons";
import { Button } from "@chakra-ui/react";
import { useEffect, useState } from "react";

export default function Player({ path }: { path: string }) {
  const [audio, setAudio] = useState(null);

  useEffect(() => {
    setAudio(new Audio(path)); // only call client
  }, []);

  return (
    <Button onClick={() => audio.play()}>
      <BellIcon>
        <audio controls>
          <source src={path} type="audio/wav" />
        </audio>
      </BellIcon>
    </Button>
  );
}
