import path from "path";
import { readInputLinesIter } from "../Common/InputParser";
import { CubeGame } from "./CubeGame";

async function main() {
    const inputPath = path.join(__dirname, 'input.txt');

    let powerSums = 0;
    for await (const line of readInputLinesIter(inputPath)) {
        const game = new CubeGame(line);
        const minimalBag = game.findMinimumCubeBag();
        const cubePower = minimalBag.blues * minimalBag.greens * minimalBag.reds;
        console.log(`Game ${game.id} has a minimal cube power of ${cubePower}`);
        powerSums += cubePower;
    }
    console.log(`Total cube power sum is ${powerSums}`);

}

main();