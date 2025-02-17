import path from 'path';
import { readInputLines } from '../Common/InputParser';
import { Trie } from '../Common/Trie';

const _digits = Array.from(Array(10).keys());
const _digitWords = [
    'zero',
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
]

function buildNumberTrie(): Trie {
    const trie = new Trie();
    _digitWords.forEach((word) => {
        trie.insert(word);
    });

    _digits.forEach((number) => {
        trie.insert(number.toString());
    });    
    return trie;
}

const numberTrie: Trie = buildNumberTrie();
const digitsByWord: Map<string, number> = new Map();
_digitWords.forEach((word, index) => {
    digitsByWord.set(word, index);
});
_digits.forEach((digit, index) => {
    digitsByWord.set(digit.toString(), index);
});

function getCalibrationValue(text: string): number {
    // find all digits
    let wordBuffer: string = '';
    const digits: number[] = [];
    let cursor: number = 0;
    let matchCursorStart: number = -1;

    while (cursor < text.length) {
        const char = text[cursor];

        wordBuffer += char;
        if (!numberTrie.startsWith(wordBuffer)) {
            cursor -= (wordBuffer.length - 1);
            wordBuffer = '';
            matchCursorStart = -1;
        }
        else {
            if (matchCursorStart == -1) {
                matchCursorStart = cursor;
            }
            if (numberTrie.search(wordBuffer)) {
                digits.push(digitsByWord.get(wordBuffer) as number);
                cursor = matchCursorStart;
                matchCursorStart = -1;
                wordBuffer = '';
            }
        }
        cursor++;
    }

    if (!digits) {
        throw new Error(`Could not generate calibration number for ${text}. No digits found.`);
    }

    // Concatenate first digit and last digit.
    // Note: first and final digit may refer to the same value.
    // e.g., A text with 'he1lo' will return 11. 
    const calibrationValue = digits[0].toString() + digits[digits.length - 1].toString();

    return Number(calibrationValue);
}

async function main() {
    const inputPath = path.join(__dirname, 'input.txt');
    const lines: string[] = await readInputLines(inputPath);

    const calibrationValues = lines.map((line) => getCalibrationValue(line));
    console.log(`Calibration Values: ${calibrationValues}`);
    const calibrationSum = calibrationValues.reduce((previous, current) => previous + current);
    console.log(`Calibration sum: ${calibrationSum}`);
}

main();