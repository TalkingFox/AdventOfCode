import path from "path";
import { readInputLinesIter } from "../Common/InputParser";
import { CubeGame } from "./CubeGame";

async function main() {
    const inputPath = path.join(__dirname, 'input.txt');

    const possibleGames: CubeGame[] = []
    for await (const line of readInputLinesIter(inputPath)) {
        const game = new CubeGame(line);
        if (game.isGamePossibleWith({ reds: 12, greens: 13, blues: 14 })) {
            possibleGames.push(game);
        }
    }
    console.log(`Playable games: ${possibleGames.map((game) => game.id).join(',')}`)
    const sum = possibleGames.map((game) => game.id).reduce((prev, cur) => prev + cur);
    console.log(`Id sum: ${sum}`);
}

main();