import { createReadStream, createWriteStream } from "fs";
import { createInterface } from "readline";
import { ensureDigitNumber } from "./WordNumberUtils";

const filePath = process.argv[2];

let calibrationNumberSum = 0;

try {
  const readLine = createInterface({
    input: createReadStream(filePath),
    crlfDelay: Infinity,
  });

  readLine.on("line", (line: string) => {
    // Use lookahead with a contained capture group to find matches without consuming the characters (example "oneight" should result in "one" and "eight")
    const numberRegex =
      /(?=(\d|(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)))/gi;

    const digits = [...line.matchAll(numberRegex)];

    if (!digits.length) {
      return;
    }

    // The second capture group is the one inside the lookahead
    const firstDigit = digits[0][1];
    const lastDigit = digits[digits.length - 1][1];

    const firstDigitNumber = ensureDigitNumber(firstDigit);
    const lastDigitNumber = ensureDigitNumber(lastDigit);

    const result = Number(`${firstDigitNumber}${lastDigitNumber}`);

    if (isNaN(result)) {
      return;
    }

    calibrationNumberSum += result;
  });

  readLine.on("close", () => {
    createWriteStream("output.txt", {
      encoding: "utf8",
      flags: "w",
    }).write(calibrationNumberSum.toString());
    console.log("Output written to output.txt");
  });
} catch (error) {
  console.error(error);
}
