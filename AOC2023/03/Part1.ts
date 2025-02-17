import path = require("path");
import { readInputAsGrid } from "../Common/InputParser";
import { Grid2D } from "../Common/Grid2d";
import { Point2d } from "../Common/Point2d";

async function main() {
    const inputPath = path.join(__dirname, 'input.txt');
    const grid: Grid2D = await readInputAsGrid(inputPath);
    const partNumbers: number[] = [];

    let partBuffer: string = '';
    let partPoints: Point2d[] = [];
    grid.rows.forEach((row, rowIndex) => {
        row.forEach((column, columnIndex) => {
            if (column >= '0' && column <= '9') {
                partBuffer += column;
                partPoints.push(new Point2d(columnIndex, rowIndex));
                return;
            }

            if (partBuffer) {
                const isPartNumber = partPoints.some((point) => {
                    const adjacentCells = grid.getAdjacentCells(point);
                    return adjacentCells.some((cell) => {
                        if (cell >= '0' && cell <= '9') {
                            return false;
                        }
                        if (cell == '.') {
                            return false;
                        }
                        return true;
                    });
                });
                if (isPartNumber) {
                    partNumbers.push(Number(partBuffer));
                }

                partBuffer = '';
                partPoints = [];
            }
            return;
        });
    });

    console.log(`Part numbers: ${partNumbers.join(',')}`);
    const partSum = partNumbers.reduce((prev, cur) => prev + cur);
    console.log(`Part numbers sum: ${partSum}`);
}

main();