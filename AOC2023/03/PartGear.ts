import { Point2d } from "../Common/Point2d";

export class PartGear {
    public gearRatio: number;

    constructor(public location: Point2d, public partNumbers: number[]) {
        this.gearRatio = partNumbers.reduce((prev, cur) => prev * cur);
    }
}