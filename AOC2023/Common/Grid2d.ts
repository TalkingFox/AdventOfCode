import { Point2d } from "./Point2d";

export class Grid2D {
    public rows: string[][] = [];
    public columnLength: number = 0;

    constructor(rows: string[]) {
        this.rows = rows.map((row) => Array.from(row));
        this.columnLength = this.rows[0].length;
    }

    public getAdjacentCells(cellPoint: Point2d): string[] {
        // Directional increments from north to northwest going clockwise.
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
        const adjacentCells: string[] = [];
        increments.forEach((increment) => {
            const checkPoint = cellPoint.add(increment);
            if (checkPoint.column < 0 || checkPoint.column >= this.columnLength) {
                return;
            }
            if (checkPoint.row < 0 || checkPoint.row >= this.rows.length) {
                return;
            }

            const checkChar = this.rows[checkPoint.row][checkPoint.column];
            adjacentCells.push(checkChar);
        });
        return adjacentCells;
    }
}