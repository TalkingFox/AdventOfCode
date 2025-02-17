import { CubeDraw } from "./CubeDraw";

export interface CubeBag {
    reds: number;
    greens: number;
    blues: number;
}

export class CubeGame {
    public id: number;
    public draws: CubeDraw[];

    constructor(input: string) {
        const idEndIndex = input.indexOf(':');
        this.id = Number(input.substring(5, idEndIndex));

        const drawInput = input.substring(idEndIndex + 1, input.length).trim();
        const drawSplits = drawInput.split(';');
        this.draws = drawSplits.map((split) => new CubeDraw(split));
    }

    public isGamePossibleWith(cubeBag: CubeBag): boolean {
        return this.draws.every((draw) =>
            draw.blueCount <= cubeBag.blues && draw.greenCount <= cubeBag.greens && draw.redCount <= cubeBag.reds
        );
    }

    public findMinimumCubeBag(): CubeBag {
        const minimalBag: CubeBag = {
            blues: 0,
            greens: 0,
            reds: 0
        };
        this.draws.forEach((draw) => {
            minimalBag.blues = Math.max(draw.blueCount, minimalBag.blues);
            minimalBag.greens = Math.max(draw.greenCount, minimalBag.greens);
            minimalBag.reds = Math.max(draw.redCount, minimalBag.reds);
        });
        return minimalBag;
    }

    public toString(): string {
        const drawStrings: string[] = [];
        this.draws.forEach((draw) => {
            drawStrings.push(draw.toString());
        });
        return `id: ${this.id}. draws: ${drawStrings.join(';')}`;
    }
}