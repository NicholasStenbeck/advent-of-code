import { createReadStream } from "fs";
import { createInterface } from "readline";

const filePath = process.argv[2];
const [red_limit, green_limit, blue_limit] = process.argv.slice(3);

const LIMITS: Record<string, number> = {
  red: Number(red_limit),
  green: Number(green_limit),
  blue: Number(blue_limit),
};

const isGamePossible = (gameData: string[]): boolean => {
  for (const hand of gameData) {
    const colors = hand.split(",").map((color) => color.trim().split(" "));
    const gameFailed = colors.some(
      ([count, name]) => LIMITS[name] < Number(count)
    );
    if (gameFailed) {
      return false;
    }
  }
  return true;
};

const getCubePower = (hands: string[]): number => {
  const maxOfColorCounts: Record<string, number> = {
    red: 0,
    green: 0,
    blue: 0,
  };

  for (const hand of hands) {
    const colors = hand.split(",").map((color) => color.trim().split(" "));
    for (const [count, name] of colors) {
      maxOfColorCounts[name] = Math.max(
        maxOfColorCounts[name] ?? 0,
        Number(count)
      );
    }
  }

  return Object.values(maxOfColorCounts).reduce(
    (acc, colorScore) => acc * colorScore,
    1
  );
};

const possibleGames: number[] = [];
let totalCubePower = 0;

try {
  const readLine = createInterface({
    input: createReadStream(filePath),
    crlfDelay: Infinity,
  });

  readLine.on("line", (line: string) => {
    const [gameName, gameData] = line.split(": ");
    const hands = gameData.split(";").map((hand) => hand.trim());

    totalCubePower += getCubePower(hands);

    if (isGamePossible(hands)) {
      const gameNumber = Number(gameName.split(" ")[1]);
      gameNumber && possibleGames.push(gameNumber);
    }
  });

  readLine.on("close", () => {
    console.log(`Total cube power: ${totalCubePower}`);
    console.log(
      `Possible games score: ${possibleGames.reduce(
        (acc, gameNumber) => acc + gameNumber,
        0
      )}`
    );
  });
} catch (error) {
  console.error(error);
}
