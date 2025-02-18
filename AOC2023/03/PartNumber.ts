import { Point2d } from "../Common/Point2d";

export class PartNumber {
    public number: number;
    private locations: Set<string>;

    constructor(number: number, locations: Point2d[]) {
        this.number = number;
        this.locations = new Set(locations.map((location) => location.toString()));
    }

    public overlaps(location: Point2d): boolean {
        return this.locations.has(location.toString());
    }
}