import path from 'path';
import { readInputLines } from '../Common/InputParser';

function getCalibrationValue(text: string): number {
    // Get all digits in contents.
    const digits: string[] = [];

    for (let i = 0; i < text.length; i++) {
        const char = text[i];
        if (char >= '0' && char <= '9') {
            digits.push(char);
        }
    }

    // Concatenate first digit and last digit.
    // Note: first and final digit may refer to the same value.
    // e.g., A text with 'he1lo' will return 11. 
    const calibrationValue = digits[0] + digits[digits.length - 1];
    
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