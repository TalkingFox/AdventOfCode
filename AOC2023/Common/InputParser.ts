import * as fs_promise from 'fs/promises';
import * as fs from 'fs';
import * as readline from 'readline/promises';
import { Grid2D } from './Grid2d';

export async function readInputLines(filepath: string): Promise<string[]> {
    const contents = await fs_promise.readFile(filepath, 'utf-8');
    const lines = contents.split(/\r?\n/);
    if (lines.length == 0) {
        return lines;
    }

    if (!lines[lines.length - 1]) {
        lines.pop();
    }
    return lines;

}

export async function* readInputLinesIter(filepath: string): AsyncGenerator<string> {
    const fileStream = fs.createReadStream(filepath);
    const readInterface = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    for await (const line of readInterface) {
        yield line;
    }
}

export async function readInputAsGrid(filepath: string): Promise<Grid2D> {
    const lines = await readInputLines(filepath);
    const grid = new Grid2D(lines);
    return grid;
}