import * as fs from 'fs/promises';

export async function readInputLines(filepath: string): Promise<string[]> {
    const contents = await fs.readFile(filepath, 'utf-8');
    const lines = contents.split(/\r?\n/);
    if (lines.length == 0) {
        return lines;
    }

    if (!lines[lines.length - 1]) {
        lines.pop();
    }
    return lines;

}