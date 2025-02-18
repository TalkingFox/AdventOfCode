export class Point2d {
    constructor(public column: number, public row: number) { }

    public add(point: Point2d): Point2d {
        return new Point2d(this.column + point.column, this.row + point.row);
    }

    public toString(): string {
        return `(${this.column},${this.row})`;
    }
}