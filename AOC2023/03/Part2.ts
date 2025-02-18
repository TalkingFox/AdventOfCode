import path = require("path");
import { readInputAsGrid } from "../Common/InputParser";
import { Grid2D } from "../Common/Grid2d";
import { Point2d } from "../Common/Point2d";
import { PartGear } from "./PartGear";

function parseNumberFrom(grid: Grid2D, point: Point2d): [number, Point2d[]] {
    let numBuffer: string = grid.rows[point.row][point.column];
    const pointsRead: Point2d[] = [point];

    // check left until non-number is found
    const leftIncrement = new Point2d(-1, 0);
    let cursor = point.add(leftIncrement);
    pointsRead.push(cursor);

    let char = grid.rows[cursor.row][cursor.column];
    while (cursor.column >= 0 && char >= '0' && char <= '9') {
        numBuffer = char + numBuffer;
        cursor = cursor.add(leftIncrement);
        pointsRead.push(cursor);
        char = grid.rows[cursor.row][cursor.column];
    }

    const rightIncrement = new Point2d(1, 0);
    cursor = point.add(rightIncrement);
    pointsRead.push(cursor);
    char = grid.rows[cursor.row][cursor.column];
    // check right until period.
    while (cursor.column < grid.columnLength && char >= '0' && char <= '9') {
        numBuffer += char;
        cursor = cursor.add(rightIncrement);
        pointsRead.push(cursor);
        char = grid.rows[cursor.row][cursor.column];
    }

    return [Number(numBuffer), pointsRead];
}

function parseGearAt(grid: Grid2D, point: Point2d): PartGear | undefined {
    const getIntersections = (increments: Point2d[]) => {
        const matches = increments.filter((increment) => {
            const checkpoint = point.add(increment);
            if (checkpoint.column < 0 || checkpoint.column >= grid.columnLength) {
                return false;
            }
            if (checkpoint.row < 0 || checkpoint.row >= grid.rows.length) {
                return false;
            }
            const checkChar = grid.rows[checkpoint.row][checkpoint.column];
            return checkChar >= '0' && checkChar <= '9';
        })
        return matches.map((match) => point.add(match));
    };

    const increments = [
        new Point2d(0, -1),     // N
        new Point2d(1, -1),     // NE
        new Point2d(1, 0),      // E
        new Point2d(1, 1),      // SE
        new Point2d(0, 1),      // S
        new Point2d(-1, 1),    // SW
        new Point2d(-1, 0),     // W
        new Point2d(-1, -1),    // NW
    ];
    const intersections = getIntersections(increments);
    const checkedIntersections = new Set<string>();

    const partNumbers: number[] = [];
    intersections.forEach((intersection) => {
        if (checkedIntersections.has(intersection.toString())) {
            return;
        }

        const [partNumber, checkedPoints] = parseNumberFrom(grid, intersection);
        partNumbers.push(partNumber);
        checkedPoints.forEach((checkedPoint) => {
            checkedIntersections.add(checkedPoint.toString());
        });
    });

    if (partNumbers.length != 2) {
        return;
    }
    const gear = new PartGear(point, partNumbers);
    return gear;
}

async function main() {
    const inputPath = path.join(__dirname, 'input.txt');
    const grid: Grid2D = await readInputAsGrid(inputPath);
    let partGears: PartGear[] = [];

    grid.rows.forEach((row, rowIndex) => {
        row.forEach((column, columnIndex) => {
            const point = new Point2d(columnIndex, rowIndex);
            if (column == '*') {
                const gear = parseGearAt(grid, point);
                if (gear) {
                    partGears.push(gear);
                }
            }
        });
    });

    console.log(`Found ${partGears.length} gears.`);
    const ratioSum: number = partGears
        .map((gear) => gear.gearRatio)
        .reduce((prev, cur) => prev + cur);
    console.log(`Sum of gear ratios is ${ratioSum}`);
}

main();
